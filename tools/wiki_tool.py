# tools/wiki_tool.py

import requests

from urllib.parse import quote


def get_wiki_summary(topic: str):
    encoded_topic = quote(topic)

    try:
        

        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            f"{encoded_topic}"
        )

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent":
                "LangGraphAssistant/1.0"
            }
        )

        response.raise_for_status()

        data = response.json()

        return {

            "success": True,

            "title": data.get("title"),

            "summary": data.get("extract")
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }