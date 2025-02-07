import requests
from bs4 import BeautifulSoup
import duckduckgo_search as ddg
from typing import List, Dict
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.constants import ErrorMessage, WEB_SCRAP_HEADER
def fetch_search_results(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Fetch search results from DuckDuckGo."""
    dgs = ddg.DDGS()
    return dgs.text(query, max_results=max_results)

def extract_text_from_url(url: str) -> str:
    """Fetch and extract main text content from a given URL."""
    headers = WEB_SCRAP_HEADER
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text,"html.parser")
        text = " ".join([p.get_text() for p in soup.find_all("p")])
        return text.strip()
    except requests.RequestException as e:
        print(ErrorMessage.FETCH_ERROR.format(str(e)))
        return ""

def get_web_scrap_documents(query: str, max_results: int = 50) -> List[Document]:
    """Fetch and process web content for vector search."""
    doc_list = [ Document(
                    page_content=extract_text_from_url(data["href"]),
                    metadata={'url':data["href"]}
                )
        for data in fetch_search_results(query, max_results)
    ]
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=200,
        chunk_overlap=0,
        is_separator_regex=False,
    )
    doc_list = text_splitter.split_documents(doc_list)

    return doc_list


