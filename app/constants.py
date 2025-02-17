"""
This module contains constants and enumerations used throughout the application.
"""

from enum import StrEnum

AUTH_HEADER={"WWW-Authenticate": "Bearer"}

class TokenType(StrEnum):
    '''Token Type Enum'''
    BEARER="bearer"

GENERAL_TYPE_ERROR="data must be a {} model"
ALLOWED_FILE_TYPES = ['pdf','docx']

class LoggingMessages:
    """
    Class containing constant logging messages used throughout the application.
    """
    FUNCTION_START = "Process of function started."
    FUNCTION_END = "Process of function ended."
    APPLICATION_STARTED = "Application started."
    START_CONVERSATION = "Conversation Endpoint has been called "
    EMBEDDING_STARTED = "Embedding Started for File {}"
    EMBEDDING_ENDED = "Embedding ended for the file {} "
    DOCUMENT_PARSER_STTARTED = "Document Parsing is started"
    DOCUMENT_PARSER_END = "Document Parsing is end "
    LLM_CALL_INNITIATE="Message has been send to LLM Model"
    LLM_RESPONSE_RECIEVED="LLM Response has been recieved successfully"