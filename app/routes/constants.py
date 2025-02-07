class RoutingPoints:
    CREATE_USER = '/user'
    LOGIN_USER = '/login'
    GET_USER = '/user'
    CREATE_NEW_CONVERSATION='/conversation'
    GET_CONVERSATION_LIST='/conversation'
    GET_CONVERSATION='/conversation/{conversation_id}'
    CHAT_CONVERSATION='/conversation/{conversation_id}'

class RoutingCategory:
    AUTH = 'User Auth'
    VIEW = 'View User'
    CONVERSATION= "Chat Conversation"

class ErrorMessages:
    EMAIL_ALREADY_TAKEN = 'email is already taken'
    USERNAME_ALREADY_TAKEN = 'username is already taken'
    ALREADY_TAKEN = "{} is already Taken"
    INCORRECT_CREDENTIALS = "Incorrect username or password"
    CONVERSATION_NOT_EXIST= 'Conversation not exist'