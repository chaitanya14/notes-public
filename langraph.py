import os
import json
import yaml
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from openai import AzureOpenAI

# ---- Azure OpenAI setup ----
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_API_BASE")
)

deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4")

# ---- Schema Definition ----
schema = {
    "title": {
        "type": "string",
        "description": "Name of your API",
        "required": True
    },
    "version": {
        "type": "string",
        "description": "API version",
        "required": True,
        "default": "1.0"
    },
    "public": {
        "type": "boolean",
        "description": "Is the API public?",
        "required": False,
        "default": True
    },
    "max_users": {
        "type": "integer",
        "description": "Maximum number of users allowed",
        "required": False
    },
    "env": {
        "type": "string",
        "description": "Deployment environment",
        "enum": ["dev", "staging", "prod"],
        "required": False,
        "default": "dev"
    }
}

# ---- LangGraph State ----
class ConfigState(TypedDict):
    config: dict
    current_field: Optional[str]

# ---- Field Selector ----
def pick_next_field(state: ConfigState) -> ConfigState:
    config = state["config"]

    for field, meta in schema.items():
        if meta.get("required", False) and field not in config:
            state["current_field"] = field
            return state

    for field, meta in schema.items():
        if field not in config:
            state["current_field"] = field
            return state

    state["current_field"] = None
    return state

# ---- Ask User Prompt ----
def ask_field(state: ConfigState) -> str:
    field = state["current_field"]
    if not field:
        return "__COMPLETE__"

    meta = schema[field]
    if "enum" in meta:
        return f"{meta['description']} Choose one: {', '.join(meta['enum'])}"
    return f"{meta['description']} ({meta['type']})"

# ---- Input Parser & Validator ----
def parse_input(user_input: str, field: str) -> Optional[any]:
    meta = schema[field]
    field_type = meta["type"]

    try:
        if "enum" in meta:
            if user_input not in meta["enum"]:
                raise ValueError("Invalid choice")
            return user_input
        elif field_type == "string":
            return str(user_input)
        elif field_type == "integer":
            return int(user_input)
        elif field_type == "boolean":
            return user_input.lower() in ["true", "yes", "1"]
    except:
        return None

    return None

# ---- Store Input ----
def store_response(state: ConfigState, user_input: str) -> ConfigState:
    field = state["current_field"]
    value = parse_input(user_input, field)
    if value is not None:
        state["config"][field] = value
        return state
    else:
        print(f"❌ Invalid input for '{field}'. Please try again.")
        return state

# ---- Add Defaults ----
def apply_defaults(state: ConfigState) -> ConfigState:
    for field, meta in schema.items():
        if field not in state["config"] and "default" in meta:
            state["config"][field] = meta["default"]
    return state

# ---- LLM Suggestion ----
def get_llm_suggestion(field: str) -> str:
    meta = schema[field]
    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant that helps users fill out API configuration fields."
        },
        {
            "role": "user",
            "content": f"What is a good value for the field '{field}'? Description: {meta['description']}. If it has choices: {meta.get('enum', 'N/A')}."
        }
    ]
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# ---- Output Formatter ----
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
builder.add_node("ask_field", ask_field)
builder.add_node("store_response", store_response)

builder.add_edge("pick_next", "ask_field")
builder.add_conditional_edges(
    "ask_field",
    lambda prompt: END if prompt == "__COMPLETE__" else "store_response"
)
builder.add_edge("store_response", "pick_next")

graph = builder.compile()

# ---- Run the Agent ----
def run_agent(partial_config: Optional[dict] = None):
    state: ConfigState = {
        "config": partial_config if partial_config else {},
        "current_field": None
    }

    print("🛠️  Let's build your config. Type 'suggest' to get a value from AI.\n")

    while True:
        state = graph.invoke(state)
        field = state["current_field"]

        if not field:
            break

        prompt = ask_field(state)
        user_input = input(f"> {prompt}\n> ").strip()

        if user_input.lower() == "suggest":
            suggestion = get_llm_suggestion(field)
            print(f"🤖 Suggested value: {suggestion}")
            user_input = input(f"Use this value? [Y/n]: ").strip().lower()
            if user_input in ["", "y", "yes"]:
                state["config"][field] = parse_input(suggestion, field)
                continue
            else:
                continue  # re-ask

        state = store_response(state, user_input)

    state = apply_defaults(state)
    output_config(state["config"])

# ---- Start It ----
if __name__ == "__main__":
    run_agent()