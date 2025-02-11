from enum import StrEnum
AUTH_HEADER={"WWW-Authenticate": "Bearer"}

class TokenType(StrEnum):
    BEARER="bearer"

GEBNERAL_TYPE_ERROR="data must be a {} model"
ALLOWED_FILE_TYPES = ['pdf','docx']