"""
Your API call methods should be defined here.
You can use the `@tool` decorator to define a tool.
The tool name will be the function name,
and the description will be the docstring of the function.
No need to call the functions here,
they will be called by the agent when needed. 
"""

import os
import requests

from dotenv import load_dotenv
from langchain_core.tools import tool

from config.loader import load_config


load_dotenv()

config = load_config()


# ==========================================================
# WEATHER TOOL
# ==========================================================

@tool
def weather(city: str) -> dict:
    """
    Get current weather and upcoming forecast information
    for a city.

    Use this tool for:
    - Current weather
    - Rain predictions
    - Weather today
    - Weather tomorrow
    - Temperature forecasts
    - Umbrella recommendations
    """

    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = "https://api.openweathermap.org/data/2.5/forecast"

    response = requests.get(
        url,
        params={
            "q": city,
            "appid": api_key,
            "units": "metric"
        },
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    current = data["list"][0]

    forecast = []

    for item in data["list"][:8]:
        forecast.append({
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "description": item["weather"][0]["description"],
            "rain": item.get("rain", {}).get("3h", 0)
        })

    return {
    "city": data["city"]["name"],
    "country": data["city"]["country"],
    "current": {
        "temperature": current["main"]["temp"],
        "feels_like": current["main"]["feels_like"],
        "humidity": current["main"]["humidity"],
        "description": current["weather"][0]["description"]
    },
    "forecast": forecast
}

# ==========================================================
# CURRENCY TOOL
# ==========================================================

@tool
def currency_exchange(
    from_currency: str,
    to_currency: str
) -> dict:
    """
    Get currency exchange rate.
    """

    url = (
        f"{config['apis']['currency_exchange']['base_url']}"
        f"/{from_currency.upper()}"
    )

    response = requests.get(
        url,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    rate = data["rates"][to_currency.upper()]

    return {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "exchange_rate": rate
    }


# ==========================================================
# NEWS TOOL
# ==========================================================

@tool
def news(topic: str) -> dict:
    """
    Get latest news about a topic.
    """

    api_key = os.getenv("NEWS_API_KEY")

    url = config["apis"]["news"]["base_url"]

    response = requests.get(
        url,
        params={
            "q": topic,
            "apiKey": api_key,
            "pageSize": 5
        },
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    articles = []

    for article in data.get("articles", [])[:5]:

        articles.append(
            {
                "title": article["title"],
                "source": article["source"]["name"],
                "url": article["url"]
            }
        )

    return {
        "topic": topic,
        "articles": articles
    }


# ==========================================================
# WIKIPEDIA TOOL
# ==========================================================

@tool
def wikipedia(topic: str) -> dict:
    """
    Search Wikipedia and return a summary.
    """

    url = (
        f"{config['apis']['wikipedia']['base_url']}"
        f"/{topic}"
    )

    response = requests.get(
        url,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    return {
        "title": data.get("title"),
        "summary": data.get("extract")
    }


TOOLS = [
    weather,
    currency_exchange,
    news,
    wikipedia
]