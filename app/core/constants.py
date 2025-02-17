'''core constant module'''
from enum import StrEnum

MSG_INVALID_CREDENTIALS="Could not validate credentials"
class UserID(StrEnum):
    '''User ID Enum'''
    USERNAME = 'username'
    EMAIL = 'email'
