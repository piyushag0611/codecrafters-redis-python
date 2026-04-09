from ..redisKVStore import *

def Type(requestParams):

    value = get_key(requestParams[0])
    _type = str(type(value))
    response = f"+{str.lower(_type)}\r\n"
    return response

