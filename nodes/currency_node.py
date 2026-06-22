from tools.currency_tool import (
    convert_currency
)


def currency_node(state):

    params = state["tool_input"]

    amount = params["amount"]

    from_currency = (
        params["from_currency"]
    )

    to_currency = (
        params["to_currency"]
    )

    result = convert_currency(
        amount,
        from_currency,
        to_currency
    )

    return {
        "tool_result": result
    }