from ..redisKVStore import *

def Type(requestParams):

    value = get_key(requestParams[0])
    if (isinstance(value, str)):
        _type = "string"
    elif (isinstance(value, list)):
        _type = "list"
    else:
        _type = "none"
    response = f"+{_type}\r\n"
    return response

