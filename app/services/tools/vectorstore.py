from langchain_community.vectorstores import FAISS
from typing import Dict 
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS



index = faiss.IndexFlatL2(len(embed_model.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embed_model,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)



def vector_search_order(query: str, web_scrap_data:dict) -> Dict[str, str]:
