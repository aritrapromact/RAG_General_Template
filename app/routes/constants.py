class RoutingPoints:
    '''Contains Routing Constant'''
    CREATE_USER = '/user'
    LOGIN_USER = '/login'
    GET_USER = '/user'
    CREATE_NEW_CONVERSATION='/conversation'
    GET_CONVERSATION_LIST='/conversation'
    GET_CONVERSATION='/conversation/{conversation_id}'
    CHAT_CONVERSATION='/conversation/{conversation_id}'
    UPLOAD_DOCUMENT='/upload'

class RoutingCategory:
    '''contains Catagory of Routing Points'''
    AUTH = 'User Auth'
    VIEW = 'View User'
    CONVERSATION= "Chat Conversation"
    UPLOAD= ' Document Upload'

class ErrorMessages:
    '''Containd Constant Error Messages '''
    EMAIL_ALREADY_TAKEN = 'email is already taken'
    USERNAME_ALREADY_TAKEN = 'username is already taken'
    ALREADY_TAKEN = "{} is already Taken"
    INCORRECT_CREDENTIALS = "Incorrect username or password"
    CONVERSATION_NOT_EXIST= 'Conversation not exist'
    EMPTY_FILENAME_ERROR="File name is empty"
    INDEX_NOT_FOUND= "Index is not found"
