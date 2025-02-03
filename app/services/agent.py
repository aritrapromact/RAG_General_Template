from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from app.config.settings import GROQ_API_KEY,GROQ_MODEL_NAME
from langchain_core.documents import Document
from typing import List
from app.services.tools import fetch_search_results
from app.services.tools.vectorstore import vector_search_order

from app.services.prompts import default_str_template_prompt

AGENT_CONFIG = {"configurable": {"thread_id": 42}}
# Define the tools for the agent to use
@tool
def deep_search_and_filter(query: str) -> List[Document]:
    """Call to surf the web. and get Detailed Content """
    outline_data = vector_search_order(query)
    return outline_data

@tool
def shallow_search_result(query:str) ->str:
    """Shallow Web Search Yools 
    Using given Query search on web and return the basic outline information of each web site
    Useful when there is very little search information required """
    outline_data = fetch_search_results(query)
    return [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in outline_data]

tools = [shallow_search_result]

model = ChatGroq(model=GROQ_MODEL_NAME, temperature=0, api_key=GROQ_API_KEY)

# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

react_agent = create_react_agent(model, tools, checkpointer=checkpointer)



def test (): 
# Use the agent
    final_state = react_agent.invoke(
        {"messages": [{"role": "user", "content": "Who own golden boot in 2010?"}]},
        config={"configurable": {"thread_id": 42}}
    )
    # print(final_state["messages"][-1].content)
    print(final_state["messages"][-1])

    return final_state
if __name__ == '__main__':
    test()

