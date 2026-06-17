def response_node(state):

    print("Response Node Executed")

    return {
        "final_response":
            f"Tool used: {state.get('tool_result')}"
    }