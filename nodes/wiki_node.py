from tools.wiki_tool import (
    get_wiki_summary
)


def wiki_node(state):

    params = state["tool_input"]

    topic = params["topic"]

    result = get_wiki_summary(topic)
    print("\n===== WIKI RESULT =====")
    print(result)

    return {
        "tool_result": result
    }