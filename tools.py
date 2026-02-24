import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(query: str):
    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )
    return response