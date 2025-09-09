from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import StructuredTool
from ddgs import DDGS
from langchain.agents import create_react_agent


def search_tool(query: str) -> str:
    with DDGS() as ddgs:
        results = [r["title"] + ": " + r["href"] for r in ddgs.text(query, max_results=3)]
    return "\n".join(results)

search = StructuredTool.from_function(
    func=search_tool,
    name="search",
    description="A tool for searching the web.",
    return_direct=True
)


def get_tools() -> list[StructuredTool]:
    """
    Get the list of tools.
    """
    return [search]