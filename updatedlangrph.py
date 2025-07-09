import os
import json
import yaml
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from openai import AzureOpenAI

# ---- Azure OpenAI Setup ----
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_API_BASE")
)
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4")

# ---- Example Nested Schema ----
schema = {
    "title": {
        "type": "string",
        "description": "API name",
        "required": True,
        "suggestions": ["User Service", "Inventory API"]
    },
    "database": {
        "type": "object",
        "description": "Database settings",
        "required": True,
        "properties": {
            "host": {
                "type": "string",
                "description": "Database host",
                "required": True,
                "suggestions": ["localhost", "db.internal"]
            },
            "port": {
                "type": "integer",
                "description": "Database port",
                "required": True,
                "suggestions": ["5432", "3306"]
            }
        }
    },
    "features": {
        "type": "array",
        "description": "Enabled features",
        "items": {
            "type": "string"
        },
        "required": False,
        "suggestions": ["logging", "metrics", "tracing"]
    }
}

# ---- State Definition ----
class ConfigState(TypedDict):
    config: dict
    current_field: Optional[list]  # path like ['database', 'host']

# ---- Schema Helpers ----
def get_schema_at_path(schema_node, path):
    for key in path:
        if "type" in schema_node and schema_node["type"] == "array":
            schema_node = schema_node["items"]
        elif "properties" in schema_node:
            schema_node = schema_node["properties"][key]
        else:
            schema_node = schema_node[key]
    return schema_node

def set_nested_value(d, path, value):
    for key in path[:-1]:
        d = d.setdefault(key, {})
    d[path[-1]] = value

def get_nested_value(d, path):
    for key in path:
        d = d.get(key, {})
    return d

# ---- Field Selection ----
def find_next_field(schema_node, config_node, path=None):
    if path is None:
        path = []

    for key, meta in schema_node.items():
        current_path = path + [key]
        config_val = config_node.get(key)

        if meta["type"] == "object":
            nested_schema = meta.get("properties", {})
            nested_config = config_node.get(key, {})
            result = find_next_field(nested_schema, nested_config, current_path)
            if result:
                return result

        elif meta["type"] == "array":
            if not config_val:
                return current_path

        else:
            if meta.get("required", False) and config_val is None:
                return current_path

    return None

def pick_next_field(state: ConfigState) -> ConfigState:
    path = find_next_field(schema, state["config"])
    state["current_field"] = path
    return state

# ---- Prompting ----
def ask_field(state: ConfigState) -> str:
    path = state["current_field"]
    if not path:
        return "__COMPLETE__"
    meta = get_schema_at_path(schema, path)
    label = ".".join(path)
    if "enum" in meta:
        return f"{label} - {meta['description']} Choose one: {', '.join(meta['enum'])}"
    return f"{label} - {meta['description']} ({meta['type']})"

# ---- LLM Suggestion ----
def get_llm_suggestion(path: list) -> str:
    meta = get_schema_at_path(schema, path)
    field = ".".join(path)
    suggestions = meta.get("suggestions", [])
    enum_values = meta.get("enum", [])

    system_prompt = "You are a helpful assistant that strictly suggests a value from the given list. Do not make up values."
    if suggestions:
        suggestion_text = f"Allowed suggestions: {', '.join(suggestions)}"
    elif enum_values:
        suggestion_text = f"Choose one of: {', '.join(enum_values)}"
    else:
        suggestion_text = ""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Suggest a value for '{field}'. Description: {meta['description']}. {suggestion_text}. Only return the value."}
    ]

    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content.strip()

# ---- Input Parsing ----
def parse_input(user_input: str, meta: dict) -> Optional[any]:
    try:
        if "enum" in meta:
            if user_input not in meta["enum"]:
                raise ValueError("Invalid enum choice")
            return user_input
        elif meta["type"] == "string":
            return user_input
        elif meta["type"] == "integer":
            return int(user_input)
        elif meta["type"] == "boolean":
            return user_input.lower() in ["true", "yes", "1"]
        elif meta["type"] == "array":
            return [i.strip() for i in user_input.split(",")]
    except:
        return None

# ---- Store Response ----
def store_response(state: ConfigState, user_input: str) -> ConfigState:
    path = state["current_field"]
    meta = get_schema_at_path(schema, path)
    value = parse_input(user_input, meta)

    if value is not None:
        set_nested_value(state["config"], path, value)
    else:
        print(f"❌ Invalid input for {'.'.join(path)}. Try again.")

    return state

# ---- Defaults (optional) ----
def apply_defaults(state: ConfigState) -> ConfigState:
    # Optional: Apply default values if needed
    return state

# ---- Output ----
def output_config(config: dict):
    format_choice = input("✅ Config complete! Output as JSON or YAML? [json/yaml]: ").strip().lower()
    if format_choice == "yaml":
        print("\n--- YAML Output ---")
        print(yaml.dump(config, sort_keys=False))
    else:
        print("\n--- JSON Output ---")
        print(json.dumps(config, indent=2))

# ---- LangGraph Setup ----
builder = StateGraph(ConfigState)
builder.set_entry_point("pick_next")
builder.add_node("pick_next", pick_next_field)
builder.add_node("store_response", store_response)
builder.add_edge("store_response", "pick_next")
graph = builder.compile()

# ---- Run Loop ----
def run_agent(partial_config: Optional[dict] = None):
    state: ConfigState = {
        "config": partial_config if partial_config else {},
        "current_field": None
    }

    print("🛠️  Let's build your config. Type 'suggest' to get a value from AI.\n")

    while True:
        state = graph.invoke(state)
        path = state["current_field"]
        if not path:
            break

        prompt = ask_field(state)
        user_input = input(f"> {prompt}\n> ").strip()

        if user_input.lower() == "suggest":
            suggestion = get_llm_suggestion(path)
            print(f"🤖 Suggested: {suggestion}")
            confirm = input("Use this? [Y/n]: ").strip().lower()
            if confirm in ["", "y", "yes"]:
                store_response(state, suggestion)
                continue
            else:
                continue  # re-ask

        state = store_response(state, user_input)

    state = apply_defaults(state)
    output_config(state["config"])

# ---- Run It ----
if __name__ == "__main__":
    run_agent()