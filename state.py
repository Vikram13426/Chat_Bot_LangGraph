from typing import TypedDict


class AgentState(TypedDict):
    user_query: str

    route: str

    tool_input: dict

    tool_result: dict

    final_response: str