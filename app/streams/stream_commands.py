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
    elementId = requestParams[1]
    [time, sequenceNum] = [int(num) for num in elementId.split("-")]
    elementDict = {"id":elementId}
    i = 2
    while (i < len(requestParams)):
        elementDict[requestParams[i]]  = requestParams[i+1]
        i += 2

    value = get_key(key)
    if (value is None):
        set_key(key, [])
        if (time == 0 and sequenceNum == 0):
            error = "-ERR The ID specified in XADD must be greater than 0-0\r\n"
            return error
    if (isinstance(value, list) and len(value) > 0):
        prev_elem = value[-1]
        [prev_time, prev_num] = [int(num) for num in prev_elem.id.split("-")]
        if (prev_time > time or (prev_time == time and prev_num > sequenceNum)):
            error = "-ERR The ID specified in XADD is equal or smaller than the target stream top item\r\n"
            return error
        
    append_items(key, [elementDict])
    return formBulkString(elementId)

