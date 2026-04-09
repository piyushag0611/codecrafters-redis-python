from .respParser import parser, formBulkString
from .redisKVStore import *

def Ping(_):

    response = "+PONG\r\n"
    return response

def Echo(requestParams):

    response = formBulkString(requestParams[0])
    return response

def Get(requestParams):

    value = get_key(requestParams[0])
    if (value == None):
        response = "$-1\r\n"
    else:
        response = formBulkString(value)
    return response

def Rpush(requestParams):

    value = get_key(requestParams[0])
    if (value == None):
        set_key(requestParams[0], [])
    
    current_len = append_items(requestParams[0], requestParams[1:])
    response = f":{current_len}\r\n"
    return response

def Lpush(requestParams):

    value = get_key(requestParams[0])
    if (value == None):
        set_key(requestParams[0], [])
    
    current_len = prepend_items(requestParams[0], requestParams[1:])
    response = f":{current_len}\r\n"
    return response

def Lrange(requestParams):

    key = requestParams[0]
    start = int(requestParams[1])
    stop = int(requestParams[2])
    items = get_items(key, start, stop)
    response = f"*{len(items)}\r\n"
    for item in items:
        response += formBulkString(item)
    return response

def Llen(requestParams):

    value = get_key(requestParams[0])
    if (value == None or not isinstance(value, list)):
        _length = 0
    else:
        _length = len(value)
    response = f":{_length}\r\n"
    return response

def Lpop(requestParams):

    key = requestParams[0]
    numElements = 1 if (len(requestParams) == 1) else int(requestParams[1])
    itemsRemoved = remove_items(key, numElements)
    if (numElements == 1 and len(itemsRemoved) == 1):
        response = formBulkString(itemsRemoved[0])
    elif(len(itemsRemoved) > 1):
        response = f"*{len(itemsRemoved)}\r\n"
        for item in itemsRemoved:
            response += formBulkString(item)
    else:
        response = "$-1\r\n"
    return response

def Blpop(requestParams):

    key = requestParams[0]
    items = bl_pop(key, int(requestParams[1]))
    if (len(items) == 0):
        response = "*-1\r\n"
    else:
        response = "*2\r\n"
        response += formBulkString(key) + formBulkString(items[0])
    return response


def Set(requestParams):

    if (len(requestParams) >= 2):
        key = requestParams[0]
        value = requestParams[1]
        timeValue = None
        if (len(requestParams) > 2):
            
            for i in range(2, len(requestParams), 2):
                optionName = requestParams[i].lower()
                if optionName == "ex":
                    timeValue = 1000 * int(requestParams[i+1])
                    break
                elif optionName == "px":
                    timeValue = int(requestParams[i+1])
                    break
                else:
                    pass

        set_key(key, value, timeValue)

        response = "+OK\r\n"
    
    else:
        response = "+FAIL\r\n"
    return response
