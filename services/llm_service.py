from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from config.loader import load_config

load_dotenv()

config = load_config()

llm = ChatGoogleGenerativeAI(
    model=config["llm"]["model"],
    temperature=config["llm"]["temperature"]
)