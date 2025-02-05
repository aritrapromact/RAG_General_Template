from typing import Any
from langchain import hub 
from typing import Dict, List , Any 
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables import RunnableConfig
from app.config.settings import AGENT_CONFIG_RUNABLE
from app.services.tools import tool_list
from app.config.settings import default_llm_model as model 

prompt = hub.pull("hwchase17/react")


AGENT_CONFIG = RunnableConfig(configurable=AGENT_CONFIG_RUNABLE)
react_agent = create_react_agent(llm= model, tools=tool_list, prompt=prompt)
agent = create_react_agent(model, tool_list, prompt)
agent_executor = AgentExecutor(agent=agent, 
                            tools=tool_list,
                            verbose=True,
                            handle_parsing_errors=True,
                            return_intermediate_steps=True )



def get_resource_from_agent_response(response: Dict[str, Any] )-> List[dict]:
    if steps := response.get('intermediate_steps') :
        last_step = steps[-1]
        if last_step[0].tool == 'deep_search_and_filter':
            return [doc.metadata for doc in last_step[1]] 
        elif last_step[0].tool == 'shallow_search_result':
            return last_step[1]
        elif last_step[0].tool == 'tavily_search_results_json':
            return last_step[1]
       