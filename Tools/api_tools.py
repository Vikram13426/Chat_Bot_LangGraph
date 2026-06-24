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
def currency(
    from_currency: str,
    to_currency: str,
    amount: float = 1
) -> dict:
    """
    Convert currencies and retrieve live exchange rates.

    Use this tool when users ask about:

    - Currency conversion
    - Exchange rates
    - Forex rates
    - Dollar rate
    - Euro rate
    - Yen rate
    - Currency comparison

    Examples:

    - Convert 100 USD to INR
    - USD to INR rate
    - Current EUR to USD rate
    - How much is 500 GBP in INR?

    Returns live exchange rate data.
    """

    api_key = os.getenv("EXCHANGE_RATE_API_KEY")

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency.upper()}"

    response = requests.get(url, timeout=15)

    response.raise_for_status()

    data = response.json()

    if data["result"] != "success":
        return {
            "error": "Unable to retrieve exchange rates."
        }

    rate = data["conversion_rates"].get(
        to_currency.upper()
    )

    if not rate:
        return {
            "error": f"Unsupported currency: {to_currency}"
        }

    converted_amount = round(
        amount * rate,
        2
    )

    return {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "amount": amount,
        "exchange_rate": rate,
        "converted_amount": converted_amount,
        "last_updated": data.get(
            "time_last_update_utc"
        )
    }


# ==========================================================
# NEWS TOOL
# ==========================================================




CATEGORY_MAP = {
    "technology": "technology",
    "sports": "sports",
    "business": "business",
    "science": "science",
    "health": "health",
    "entertainment": "entertainment",
}

COUNTRY_MAP = {
    "america": "us",
    "usa": "us",
    "united states": "us",
    "india": "in",
    "japan": "jp",
    "china": "cn",
    "canada": "ca",
    "australia": "au",
    "uk": "gb",
    "united kingdom": "gb",
}


@tool
def news(query: str = "latest news") -> dict:
    """
    Get latest news.

    Supports:
    - General headlines
    - Category news
    - Country news
    - Topic specific news

    Examples:
    - latest news
    - technology news
    - sports news
    - news in india
    - OpenAI news
    - Tesla news
    """

    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        return {"error": "NEWS_API_KEY not configured"}

    query_lower = query.lower().strip()

    articles = []

    # --------------------------------------------------
    # CATEGORY NEWS
    # --------------------------------------------------

    if query_lower in CATEGORY_MAP:

        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                "category": CATEGORY_MAP[query_lower],
                "language": "en",
                "pageSize": 5,
                "apiKey": api_key
            },
            timeout=15
        )

        mode = "category"

    # --------------------------------------------------
    # COUNTRY NEWS
    # --------------------------------------------------

    elif query_lower in COUNTRY_MAP:

        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                "country": COUNTRY_MAP[query_lower],
                "pageSize": 5,
                "apiKey": api_key
            },
            timeout=15
        )

        mode = "country"

    # --------------------------------------------------
    # GENERAL HEADLINES
    # --------------------------------------------------

    elif query_lower in [
        "latest news",
        "breaking news",
        "today news",
        "today's news",
        "current news"
    ]:

        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                "language": "en",
                "pageSize": 5,
                "apiKey": api_key
            },
            timeout=15
        )

        mode = "headlines"

    # --------------------------------------------------
    # TOPIC SEARCH
    # --------------------------------------------------

    else:

        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": query,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 5,
                "apiKey": api_key
            },
            timeout=15
        )

        mode = "topic"

    response.raise_for_status()

    data = response.json()

    for article in data.get("articles", []):

        articles.append({
            "title": article.get("title"),
            "source": article.get("source", {}).get("name"),
            "published_at": article.get("publishedAt"),
            "description": article.get("description"),
            "url": article.get("url")
        })

    return {
        "mode": mode,
        "query": query,
        "article_count": len(articles),
        "articles": articles
    }
# ==========================================================
# WIKIPEDIA TOOL
# ==========================================================




@tool
def wiki(topic: str) -> dict:
    """
    Retrieve encyclopedic information from Wikipedia.

    Use this tool when users ask about:

    - What is X?
    - Who is X?
    - Tell me about X
    - Explain X
    - History of X
    - Information about a country
    - Information about a person
    - Information about a company
    - Information about a technology
    - General knowledge topics

    Returns a concise encyclopedia-style summary.
    """

    try:

        url = "https://en.wikipedia.org/w/api.php"

        headers = {
            "User-Agent": "AgenticAIAssistant/1.0"
        }

        response = requests.get(
            url,
            params={
                "action": "query",
                "format": "json",
                "prop": "extracts",
                "titles": topic,
                "exintro": True,
                "explaintext": True,
                "redirects": 1
            },
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        pages = data.get("query", {}).get("pages", {})

        if not pages:
            return {
                "topic": topic,
                "error": "No information found."
            }

        page = next(iter(pages.values()))

        if "missing" in page:
            return {
                "topic": topic,
                "error": f"No Wikipedia article found for '{topic}'."
            }

        title = page.get("title", topic)

        summary = page.get(
            "extract",
            "No summary available."
        )

        page_url = (
            "https://en.wikipedia.org/wiki/"
            + title.replace(" ", "_")
        )

        return {
            "topic": topic,
            "title": title,
            "summary": summary,
            "url": page_url
        }

    except requests.exceptions.Timeout:

        return {
            "topic": topic,
            "error": "Wikipedia request timed out."
        }

    except requests.exceptions.RequestException as e:

        return {
            "topic": topic,
            "error": str(e)
        }

    except Exception as e:

        return {
            "topic": topic,
            "error": str(e)
        }
        
TOOLS = [
    weather,
    currency,
    news,
    wiki
]