import re
import json
import yaml
from typing import Optional, TypedDict, Any
from langgraph.graph import StateGraph, END

# --- SCHEMA NORMALIZER ---
def normalize_openapi_schema(openapi_schema: dict) -> dict:
    required_fields = set(openapi_schema.get("required", []))
    properties = openapi_schema.get("properties", {})
    pattern_properties = openapi_schema.get("patternProperties", {})

    def normalize_field(meta, is_required=False):
        if not meta:
            return {
                "type": "any",
                "description": "No constraints",
                "required": is_required
            }

        field_type = meta.get("type", "string")
        norm = {
            "type": field_type,
            "description": meta.get("description", ""),
            "required": is_required
        }

        if "default" in meta:
            norm["default"] = meta["default"]
        if "enum" in meta:
            norm["enum"] = meta["enum"]

        if field_type == "object":
            nested_required = set(meta.get("required", []))
            nested_props = meta.get("properties", {})
            norm["properties"] = normalize_properties(nested_props, nested_required)

        elif field_type == "array":
            norm["items"] = normalize_field(meta.get("items", {"type": "string"}))

        return norm

    def normalize_properties(props, required_set):
        result = {}
        for field, meta in props.items():
            result[field] = normalize_field(meta, field in required_set)
        return result

    normalized = normalize_properties(properties, required_fields)

    if pattern_properties:
        normalized["__patternProperties__"] = {
            pattern: normalize_field(meta) for pattern, meta in pattern_properties.items()
        }

    return normalized

# --- LANGGRAPH STATE ---
class ConfigState(TypedDict):
    config: dict
    current_field: Optional[str]

# --- EXAMPLE SCHEMA ---
openapi_schema = {
    "type": "object",
    "required": ["name"],
    "properties": {
        "name": {
            "type": "string",
            "description": "Name of the resource"
        }
    },
    "patternProperties": {
        "^x-.*": {
            "type": "object",
            "description": "Dynamic x-prefixed config",
            "required": ["enabled"],
            "properties": {
                "enabled": {
                    "type": "boolean",
                    "description": "Whether feature is enabled"
                },
                "threshold": {
                    "type": "integer",
                    "description": "Threshold value"
                }
            }
        },
        "^tags-.*": {
            "type": "array",
            "description": "Dynamic tag values",
            "items": {
                "type": "string"
            }
        },
        "^z-.*": {}
    }
}

schema = normalize_openapi_schema(openapi_schema)

# --- LANGGRAPH NODES ---
def pick_next_field(state: ConfigState) -> ConfigState:
    for field, meta in schema.items():
        if field.startswith("__"):
            continue
        if meta.get("required", False) and field not in state["config"]:
            state["current_field"] = field
            return state
        if field not in state["config"]:
            state["current_field"] = field
            return state
    state["current_field"] = None
    return state

def ask_field(state: ConfigState) -> str:
    field = state["current_field"]
    if not field:
        return "__COMPLETE__"
    meta = schema[field]
    return f"{meta['description']} ({meta['type']})"

def parse_input(user_input: str, meta: dict) -> Any:
    try:
        field_type = meta.get("type")
        if field_type == "string":
            return str(user_input)
        elif field_type == "integer":
            return int(user_input)
        elif field_type == "boolean":
            return user_input.lower() in ["true", "yes", "1"]
        elif field_type == "array":
            return [item.strip() for item in user_input.split(",")]
        elif field_type == "object":
            nested = {}
            for subkey, submeta in meta.get("properties", {}).items():
                val = input(f"  > {subkey} ({submeta['type']}): ").strip()
                nested[subkey] = parse_input(val, submeta)
            return nested
        elif field_type == "any":
            return user_input
    except:
        return None

def store_response(state: ConfigState, user_input: str) -> ConfigState:
    field = state["current_field"]
    meta = schema[field]
    parsed = parse_input(user_input, meta)
    if parsed is not None:
        state["config"][field] = parsed
    else:
        print("❌ Invalid input, try again.")
    return state

# --- DEFAULTS ---
def apply_defaults(state: ConfigState) -> ConfigState:
    for field, meta in schema.items():
        if field.startswith("__"):
            continue
        if field not in state["config"] and "default" in meta:
            state["config"][field] = meta["default"]
    return state

# --- OUTPUT FORMATTER ---
def output_config(config: dict):
    choice = input("✅ Config complete! Output as JSON or YAML? [json/yaml]: ").strip().lower()
    if choice == "yaml":
        print("--- YAML ---")
        print(yaml.dump(config, sort_keys=False))
    else:
        print("--- JSON ---")
        print(json.dumps(config, indent=2))

# --- LANGGRAPH SETUP ---
builder = StateGraph(ConfigState)
builder.set_entry_point("pick_next")
builder.add_node("pick_next", pick_next_field)
builder.add_node("ask_field", ask_field)
builder.add_node("store_response", store_response)

builder.add_edge("pick_next", "ask_field")
builder.add_conditional_edges("ask_field", lambda msg: END if msg == "__COMPLETE__" else "store_response")
builder.add_edge("store_response", "pick_next")
graph = builder.compile()

# --- RUN INTERACTIVE AGENT ---
def run_agent():
    state: ConfigState = {"config": {}, "current_field": None}
    print("🧠 Let's build your config.\n")

    # Built-in prompt for static and dynamic fields
    while True:
        state = graph.invoke(state)
        field = state["current_field"]
        if not field:
            break
        prompt = ask_field(state)
        user_input = input(f"> {prompt}\n> ").strip()
        state = store_response(state, user_input)

    # Handle patternProperties interactively
    if "__patternProperties__" in schema:
        print("\n💡 Add dynamic fields (like `x-feature`, `tags-ui`, `z-anykey`). Type 'done' to finish.")
        while True:
            dyn_key = input("🔑 Dynamic key: ").strip()
            if dyn_key.lower() == "done":
                break
            matched = False
            for pattern, meta in schema["__patternProperties__"].items():
                if re.match(pattern, dyn_key):
                    val = input(f"  📥 Value for {dyn_key} ({meta['type']}): ").strip()
                    parsed = parse_input(val, meta)
                    if parsed is not None:
                        state["config"][dyn_key] = parsed
                    else:
                        print("❌ Invalid input.")
                    matched = True
                    break
            if not matched:
                print("⚠️ No matching pattern found.")

    state = apply_defaults(state)
    output_config(state["config"])

# --- START ---
if __name__ == "__main__":
    run_agent()