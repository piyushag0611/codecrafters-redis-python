from ..redisKVStore import *
from ..respParser import *

def Type(requestParams):

    value = get_key(requestParams[0])
    if (isinstance(value, str)):
        _type = "string"
    elif (isinstance(value, list)):
        if (isinstance(value[0], dict)):
            _type = "stream"
        else:
            _type = "list"
    else:
        _type = "none"
    response = f"+{_type}\r\n"
    return response

def Xadd(requestParams):

    key = requestParams[0]
    value = get_key(key)
    if (value is None):
        set_key(key, [])
    elementId = requestParams[1]
    elementDict = {"id":elementId}
    i = 2
    while (i < len(requestParams)):
        elementDict[requestParams[i]]  = requestParams[i+1]
        i += 2
    append_items(key, [elementDict])
    return formBulkString(elementId)

