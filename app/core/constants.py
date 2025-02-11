from enum import StrEnum

MSG_INVALID_CREDENTIALS="Could not validate credentials"
class USER_ID(StrEnum):
    USERNAME = 'username'
    EMAIL = 'email'

