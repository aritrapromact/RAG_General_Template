from sentence_transformers import CrossEncoder

from app.config.settings import (
    RELEVENCY_CHECK_MODEL,
    RELEVENCY_SCORE_THRESH,
    default_llm_model,
)
from app.services.RAG.prompts import default_chat_template_prompt
from app.services.RAG.vectorstore import similarity_search


def get_llm_response(query:str, user_id: str):
    retrieved_chunks = similarity_search(query=query, user_id=user_id)
    llm_chain = default_chat_template_prompt | default_llm_model
    response =   llm_chain.invoke(
        {
            "query" : query,
            "context" : '\n'.join([doc.page_content for doc in retrieved_chunks])
        }
    )
    llm_response = response.content
    cross_encoder = CrossEncoder(RELEVENCY_CHECK_MODEL)
    # Compare LLM response with retrieved chunks
    chunk_texts = [chunk.page_content for chunk in retrieved_chunks]
    pairs = [(llm_response, chunk) for chunk in chunk_texts]
    # Get relevance scores (0 to 1)
    scores = cross_encoder.predict(pairs)
    # Filter chunks based on a threshold 
    used_chunks = [retrieved_chunks[i].page_content
                    for i, score in enumerate(scores)
                        if score > RELEVENCY_SCORE_THRESH]
    return ({
        'query': query,
        "answer": llm_response,
        "references": used_chunks})

if __name__ =='__main__':
    print(get_llm_response("Who killed Thanos"))
