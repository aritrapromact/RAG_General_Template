'''This is the Prompt List'''

from langchain.prompts.chat import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

default_template_prompt = PromptTemplate.from_template(
    """
    You are an AI assistant tasked with answering user questions based on the provided\
        context in form of tags where metadata is also mentioned as properties of Tags. \
        Context are enclosed by <context> </context> tag. 
    As a response Write your answer in following Json format.
    Response Format :

    "answer" : "Write your answer here",
    "relevent_chunks" : "List of allchunks. Write all exact chunks as provided in a list that are actually used to generate the answer"


    If the context does not contain relevant information, respond with \
        "I don't know based on the available information."


    Context:
    {context}

    Question:
    {query}

    Provide a concise and accurate answer based on the context and chat history above.
    """

)
