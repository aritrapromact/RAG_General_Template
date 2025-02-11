from pathlib import Path
from typing import List

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.config.settings import EMBEDDING_MODEL_VECTOR_LENGTH, embed_model
from app.config.settings import DEFAULT_INDEX_PATH
index = faiss.IndexFlatL2(EMBEDDING_MODEL_VECTOR_LENGTH)
import faiss
def validate_index_path(index_path: str | Path | None):
    """
    Validates the provided index path.
    Parameters:
    index_path (str | Path | None): The path to the index. It can be a string, a Path object, or None.
    Returns:
    Path: The resolved Path object if the index_path is valid.
    Raises:
    Exception: If the index_path is None.
    """
    
    if index_path is None :
        raise Exception("Index Not Found")
    elif not isinstance(index_path,Path):
        index_path = Path(index_path).resolve()
        if not index_path.exists():
            raise Exception("Index Not Found")
        
    return index_path
    
def save_on_vector_store(documents : List[Document], user_id: str, index_path:str|Path|None=DEFAULT_INDEX_PATH) :
    """
        Save documents to a FAISS vector store.
        Parameters:
        documents (List[Document]): A list of documents to be added to the vector store.
        index_path (str | Path | None): The path to the existing FAISS index. If None, a new index will be created.
        Returns:
        None
    """
    user_id = str(user_id)
    if index_path and not isinstance(index_path,Path):
        index_path= Path(index_path).resolve()
    if (index_path/user_id).exists() :       
        faiss_store = FAISS.load_local(index_path/user_id, embed_model,allow_dangerous_deserialization=True)
        faiss_store.add_documents(documents)
    else:
        faiss_store = FAISS.from_documents(documents, embed_model)
    faiss_store.save_local((index_path/user_id).as_posix())

def similarity_search(query:str,  user_id: str, index_path: str|Path|None = DEFAULT_INDEX_PATH)-> List[Document]:
    """
        Perform a similarity search on the given query using the specified index path.
        Args:
            query (str): The query string to search for.
            index_path (str | Path | None, optional): The path to the index file. Defaults to DEFAULT_INDEX_PATH.
        Returns:
            List[Document]: A list of documents that are similar to the query.
        Raises:
            Exception: If the index_path is None.
    """
    user_id = str(user_id)
    index_path = validate_index_path(index_path/user_id)
    faiss_store = FAISS.load_local(index_path.as_posix(), embed_model,allow_dangerous_deserialization=True)
    results = faiss_store.similarity_search(query, k=3)
    return results

def get_retriver( user_id: str, index_path: str|Path|None = DEFAULT_INDEX_PATH): 
    user_id = str(user_id)
    index_path = validate_index_path(index_path/user_id)
    return FAISS.load_local(index_path.as_posix(), embed_model,allow_dangerous_deserialization=True).as_retriever()
    