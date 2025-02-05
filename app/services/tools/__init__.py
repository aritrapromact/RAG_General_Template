"""
This module contains the Tools that are used by the Agents Directly 
"""
from typing import List
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from app.services.tools.vectorstore import vector_search_order
from app.services.tools.search import fetch_search_results
# from app.services.prompts import default_str_template_prompt


tavily_search_tools =TavilySearchResults(
    max_results=10,
    search_depth="advanced",
    # include_answer=True,
    include_raw_content=True,
    include_images=True,
    # include_domains=[...],
    # exclude_domains=[...],
    # name="...",            # overwrite default tool name
    # description="...",     # overwrite default tool description
    # args_schema=...,       # overwrite default args_schema: BaseModel
)

@tool
def deep_search_and_filter(query: str) -> List[Document]:
    """Call to surf the web and get Detailed Content """
    outline_data = vector_search_order(query)
    return outline_data


@tool
def shallow_search_result(query:str) ->str:
    """Shallow Web Search Yools 
    Using given Query search on web and return the basic outline information of each web site
    Useful when there is very little search information required """
    outline_data = fetch_search_results(query)
    return outline_data
tool_list= [deep_search_and_filter,shallow_search_result]




