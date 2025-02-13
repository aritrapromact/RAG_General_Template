from enum import StrEnum

AUTH_HEADER={"WWW-Authenticate": "Bearer"}

class TokenType(StrEnum):
    BEARER="bearer"

GENERAL_TYPE_ERROR="data must be a {} model"
ALLOWED_FILE_TYPES = ['pdf','docx']

class LoggingMessages:
    FUNCTION_START = "Process of function started."
    FUNCTION_END = "Process of function ended."
    APPLICATION_STARTED = "Application started."
    START_CONVERSATION = "Conversation Endpoint has been called "
    EMBEDDING_STARTED = "Embedding Started for File %s"
    EMBEDDING_ENDED = "Embedding ended for the file %s "
    DOCUMENT_PARSER_STTARTED = "Document Parsing is started"
    DOCUMENT_PARSER_END = "Document Parsing is end "
    LLM_CALL_INNITIATE="Message has been send to LLM Model"
    LLM_RESPONSE_RECIEVED="LLM Response has been recieved successfully"