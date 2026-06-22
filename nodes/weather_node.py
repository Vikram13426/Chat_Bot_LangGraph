from tools.weather_tool import get_weather


def weather_node(state):

    params = state["tool_input"]

    city = params.get("city")

    if not city:
        raise ValueError(
            "Weather route requires city"
        )

    result = get_weather(city)

    return {
        "tool_result": result
    }