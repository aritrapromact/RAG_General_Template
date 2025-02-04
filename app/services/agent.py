from typing import Any
from langchain import hub 
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableConfig
from pydantic import SecretStr
from app.config.settings import GROQ_API_KEY, GROQ_MODEL_NAME, AGENT_CONFIG_RUNABLE
from app.services.tools import tool_list


prompt = hub.pull("hwchase17/react")


AGENT_CONFIG = RunnableConfig(configurable=AGENT_CONFIG_RUNABLE)
model = ChatGroq(model=GROQ_MODEL_NAME, temperature=0, api_key=SecretStr(GROQ_API_KEY))
react_agent = create_react_agent(llm= model, tools=tool_list, prompt=prompt)
agent = create_react_agent(model, tool_list, prompt)
agent_executor = AgentExecutor(agent=agent, 
                            tools=tool_list,
                            verbose=True,
                            handle_parsing_errors=True,
                            return_intermediate_steps=True )