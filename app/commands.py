from .respParser import formBulkString
from .redisKVStore import *

def Ping(_):

    response = "+PONG\r\n"
    return response

def Echo(requestParams):

    response = formBulkString(requestParams[0])
    return response

