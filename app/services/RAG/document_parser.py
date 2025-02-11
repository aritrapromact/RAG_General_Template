'''
This module provides functionality to parse PDF documents and extract text from each page.
Functions:
    parse_documents(file_content: bytes, filename: str | None = 'unknown', filetype: str = 'pdf') -> list:

'''
import io

import pymupdf
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def parse_documents(file_content:bytes, filename:str | None = 'unknown', filetype:str='pdf', file_metadata:dict = {}):
    """
        Parses the content of a PDF document from bytes and extracts text from each page.
        Args:
            file_content (bytes): The content of the PDF file in bytes.
            filename (str, optional): The name of the file. Defaults to 'unknown'.
            filetype (str, optional): The type of the file. Defaults to 'pdf'.
        Returns:
            list: A list of Document objects, each containing the text of a page and metadata including the filename, page number, and title.
        """
    pdf_stream = io.BytesIO(file_content)
    def _get_title(text:str):
        '''Extract Title from First Page'''
        for line in text:
            if line.strip():
                return line
    with pymupdf.open(filename=filename, stream=pdf_stream, filetype=filetype)  as doc:
        title = _get_title(doc[0].get_text().split('\n'))
        documents = [
            Document(
                page_content=page.get_text(),
                metadata = {
                    'filename':filename,
                    'page_number': page.number+1,
                    'title':title,
                    **file_metadata
                } ) for page in doc
        ]
    if documents:
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=512, chunk_overlap=32
        )
        documents = text_splitter.split_documents(documents)
        return documents