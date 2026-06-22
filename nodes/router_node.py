from services.llm_service import llm
from prompts.router_prompt import ROUTER_PROMPT


def router_node(state):

    user_query = state["user_query"]

    prompt = f"""
    {ROUTER_PROMPT}

    Question:
    {user_query}
    """

    response = llm.invoke(prompt)

    route = response.content.strip().lower()

    print(f"Selected Route: {route}")

    return {
        "route": route
    }