from typing import TypedDict, Optional


class AgentState(TypedDict):
    user_query: str

    route: str

    tool_result: Optional[dict]

    final_response: str