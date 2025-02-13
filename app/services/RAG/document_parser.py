'''
This module provides functionality to parse PDF documents and extract text from each page.
Functions:
    parse_documents(file_content: bytes, filename: str | None = 'unknown', filetype: str = 'pdf') -> list:

'''
import io
import re
from typing import Dict, List
from uuid import uuid4

import pymupdf
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.logging_config import logger
from app.constants import LoggingMessages


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
    logger.info(LoggingMessages.DOCUMENT_PARSER_STTARTED)
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
            chunk_size=256, chunk_overlap=16
        )
        documents = text_splitter.split_documents(documents)
        logger.info(LoggingMessages.DOCUMENT_PARSER_END)
        return documents



def context_parser_input(documents:List[Document])->str :

    """
    Parses a list of Document objects into a list of context strings formatted in XML-like tags.
    Args:
        documents (List[Document]): A list of Document objects, each containing metadata and page content.
    Returns:
        List[str]: A list of strings, each representing a document's content wrapped in a context tag with metadata attributes.
    """

    context_template = '<context {metadata}> {page_content} </context>\n'
    parsed_contexts = []
    for doc in documents:
        metadata_str = f'id="{uuid4()} "'+' '.join([f'{key}="{value}"' for key, value in doc.metadata.items()])
        context_str = context_template.format(metadata=metadata_str, page_content=doc.page_content)
        parsed_contexts.append(context_str)
    return parsed_contexts



def context_parser_output(contexts:List[str] ) -> Dict[str, str | dict]:
    """
    Parses the given context string to extract content and metadata attributes.
    Args:
        context (str): The context string containing content and metadata attributes.
    Returns:
        Dict[str, str | dict]: A dictionary with two keys:
            - "content": The extracted content as a string.
            - "metadata": A dictionary of extracted metadata attributes as key-value pairs.
    """
    content_pattern = re.compile(r"<context(.*?)>(.*?)</context>", re.DOTALL)
    if not  isinstance(contexts, list):
        contexts = [contexts]
    context_list = []
    for context in contexts:
        content_match = content_pattern.search(context)
        attributes_part = content_match.group(1).strip() if content_match else ""
        content = content_match.group(2).strip() if content_match else ""
        # Extract attributes as key-value pairs
        attributes_pattern = re.compile(r"(\w+)=\"(.*?)\"")
        attributes = dict(attributes_pattern.findall(attributes_part))
    context_list.append( {
        "content": content,
        "metadata": attributes})

    return context_list
