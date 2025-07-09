import jsonref
import yaml

def load_openapi_schema(file_path: str, schema_name: str) -> dict:
    with open(file_path, "r") as f:
        spec = yaml.safe_load(f)

    resolved = jsonref.replace_refs(spec)
    return resolved["components"]["schemas"][schema_name]

def normalize_openapi_schema(openapi_schema: dict) -> dict:
    properties = openapi_schema.get("properties", {})
    required_fields = set(openapi_schema.get("required", []))

    def normalize(prop_dict, required_set=None):
        result = {}
        for field, meta in prop_dict.items():
            norm = {
                "type": meta["type"],
                "description": meta.get("description", ""),
                "required": field in required_set if required_set else False
            }

            if "default" in meta:
                norm["default"] = meta["default"]
            if "enum" in meta:
                norm["enum"] = meta["enum"]
            if meta["type"] == "object":
                nested_required = set(meta.get("required", []))
                norm["properties"] = normalize(meta.get("properties", {}), nested_required)
            elif meta["type"] == "array":
                norm["items"] = meta["items"]

            result[field] = norm
        return result

    return normalize(properties, required_fields)