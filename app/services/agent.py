from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from app.config.settings import GROQ_API_KEY,GROQ_MODEL_NAME


from app.services.tools import fetch_search_results
from pydantic import BaseModel
# Define the tools for the agent to use
@tool
def deep_search_and_filter(query: str):
    """Call to surf the web."""
    # This is a placeholder, but don't tell the LLM that...
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "Temperature is 42 degree"

    return "It's 90 degrees and sunny."

@tool 
def shallow_search_result(query:str):
    """Shallow Web Search Yools 
    Using given Query search on web and return the basic outline information of each web site
    Useful when there is very little search information required """
    outline_data = fetch_search_results(query)
    return "\n".join (result['body'] for result in outline_data)

tools = [shallow_search_result,deep_search_and_filter]

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

