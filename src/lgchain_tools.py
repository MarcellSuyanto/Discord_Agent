from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import StructuredTool
from ddgs import DDGS
from langchain.agents import create_react_agent
import wikipedia




def get_tools() -> list[StructuredTool]:
    """
    Get the list of tools.
    """
    return []