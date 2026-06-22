from services.llm_service import llm

from prompts.response_prompt import (
    RESPONSE_PROMPT
)


def response_node(state):

    prompt = RESPONSE_PROMPT.format(
        question=state["user_query"],
        tool_result=state.get(
            "tool_result",
            {}
        )
    )

    response = llm.invoke(prompt)

    return {
        "final_response": response.content
    }