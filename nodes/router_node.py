from services.llm_service import llm

from schemas.router_schema import RouterOutput

from prompts.router_prompt import ROUTER_PROMPT


structured_llm = llm.with_structured_output(
    RouterOutput
)


def router_node(state):

    query = state["user_query"]

    prompt = f"""
    {ROUTER_PROMPT}

    User Query:
    {query}
    """

    result = structured_llm.invoke(prompt)

    print("\n===== ROUTER OUTPUT =====")
    print(result)

    return {
        "route": result.route,
        "tool_input": result.tool_input
    }