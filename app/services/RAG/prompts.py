'''This is the Prompt List'''

from langchain_core.prompts import PromptTemplate

default_chat_template_prompt = PromptTemplate.from_template(
"""
    You are an AI assistant tasked with answering user questions based on the provided context and chat history. 
    If the context does not contain relevant information, respond with "I don't know based on the available information."

    Context:
    {context}

    Question:
    {query}

    Provide a concise and accurate answer based on the context and chat history above.
    """

)
