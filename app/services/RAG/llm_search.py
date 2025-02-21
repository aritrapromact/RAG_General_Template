
import json
from typing import Any

from langfuse.callback import CallbackHandler
from sentence_transformers import CrossEncoder

from app.config.logging_config import logger
from app.config.settings import (
    LANGFUSE_CONFIG,
    RELEVENCY_CHECK_MODEL,
    RELEVENCY_SCORE_THRESH,
    default_llm_model,
)
from app.constants import LoggingMessages
from app.services.RAG.document_parser import context_parser_input, context_parser_output
from app.services.RAG.prompts import default_template_prompt
from app.services.RAG.vectorstore import similarity_search

langfuse_handler = CallbackHandler(**LANGFUSE_CONFIG)
def get_relevent_chunks(llm_response:Any, retrieved_chunks:Any):
    """
    Filters and returns relevant chunks from the retrieved chunks based on their relevance to the LLM response.
    Args:
        llm_response (Any): The response from the language model.
        retrieved_chunks (Any): A collection of chunks retrieved from a source, each containing 'page_content' and 'metadata'.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing 'content' and 'metadata' of the relevant chunks.
    """
    cross_encoder = CrossEncoder(RELEVENCY_CHECK_MODEL)
    # Compare LLM response with retrieved chunks
    chunk_texts = [chunk.page_content for chunk in retrieved_chunks]
    pairs = [(llm_response, chunk) for chunk in chunk_texts]
    # Get relevance scores (0 to 1)
    scores = cross_encoder.predict(pairs)
    # Filter chunks based on a threshold
    used_chunks = [
        {
            "content":retrieved_chunks[i].page_content,
            "metadata":retrieved_chunks[i].metadata
        } for i, score in enumerate(scores)
            if score > RELEVENCY_SCORE_THRESH
    ]
    return used_chunks

def get_llm_response(query:str, user_id: str):
    retrieved_chunks = similarity_search(query=query, user_id=user_id)
    llm_chain = default_template_prompt | default_llm_model
    logger.info(LoggingMessages.LLM_CALL_INNITIATE)
    response =   llm_chain.invoke(
        {
            "query" : query,
            "context" : context_parser_input(retrieved_chunks),
        },
        config={"callbacks": [langfuse_handler]}
    )
    llm_response = response.content
    response_json_str = llm_response[7:-3]
    response_json = json.loads(response_json_str)
    llm_answer = response_json['answer']
    relevent_chunks = response_json ['relevent_chunks']
    # resource = get_relevent_chunks(response,retrieved_chunks)

    logger.info(LoggingMessages.LLM_RESPONSE_RECIEVED)

    return ({
        'query': query,
        "answer": llm_answer,
        "resource" : context_parser_output(relevent_chunks)
    })
