from langchain_community.vectorstores import FAISS
from typing import List
from langchain_core.documents import Document
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from app.config.settings import embed_model,EMBEDDING_MODEL_VECTOR_LENGTH
from app.services.tools.search import  get_web_scrap_documents
index = faiss.IndexFlatL2(EMBEDDING_MODEL_VECTOR_LENGTH)



def vector_search_order(query: str) -> List[Document]:
    """Search the vector store for the most similar vectors to the query."""
    vector_store = FAISS(
        embedding_function=embed_model,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    web_scrap_documents = get_web_scrap_documents(query)
    vector_store.add_documents(documents=web_scrap_documents)
    search_results = vector_store.similarity_search(query)
    return search_results
