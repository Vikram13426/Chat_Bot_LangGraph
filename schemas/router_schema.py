from typing import Dict, Any, Literal

from pydantic import BaseModel


class RouterOutput(BaseModel):

    route: Literal[
        "weather",
        "news",
        "currency",
        "wiki",
        "direct"
    ]

    tool_input: Dict[str, Any]