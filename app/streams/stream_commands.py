from redisKVStore import *

def Type(requestParams):

    value = get_key(requestParams[0])
    _type = type(value)
    response = f"+{_type.lower()}\r\n"
    return response

