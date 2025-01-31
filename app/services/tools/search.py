import requests
from bs4 import BeautifulSoup
import duckduckgo_search as ddg
from typing import List, Dict

def fetch_search_results(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Fetch search results from DuckDuckGo."""
    dgs = ddg.DDGS()
    return dgs.text(query, max_results=max_results)

def extract_text_from_url(url: str) -> str:
    """Fetch and extract main text content from a given URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract visible text from paragraph tags
        text = " ".join([p.get_text() for p in soup.find_all("p")])
        return text.strip()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def get_clean_texts(query: str, max_results: int = 5) -> Dict[str, str]:
    """Fetch search results and extract text content from the URLs."""
    search_results = fetch_search_results(query, max_results)
    url_texts = {}
    
    for result in search_results:
        try :
            url = result["href"]
            text_content = extract_text_from_url(url)
            url_texts[url] = text_content
        except Exception as e:
            print(f"Error processing {result['href']}: {e}")
             
    return url_texts

