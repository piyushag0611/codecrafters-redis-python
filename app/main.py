import socket  # noqa: F401
import threading
from .respParser import parser, formBulkString
from .redisKVStore import *
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    while(True):
        conn, _ = server_socket.accept() # wait for client
        thread = threading.Thread(target = handle_conn, args=(conn,))
        thread.start()


def handle_conn(conn):

    while(True):

        request = conn.recv(1024).decode()
        (commandName, requestParams) = parser(request)

        if request is None:
            break

        if commandName == "ping":

            response = "+PONG\r\n"
        
        elif commandName == "echo":

            response = formBulkString(requestParams[0])

        elif commandName == "get":

            value = get_key(requestParams[0])
            if (value == None):
                response = "$-1\r\n"
            else:
                response = formBulkString(value)

        elif commandName == "rpush":

            value = get_key(requestParams[0])
            if (value == None):
                set_key(requestParams[0], [])
            
            current_len = append_items(requestParams[0], requestParams[1:])
            response = f":{current_len}\r\n"

        elif commandName == "lpush":

            value = get_key(requestParams[0])
            if (value == None):
                set_key(requestParams[0], [])
            
            current_len = prepend_items(requestParams[0], requestParams[1:])
            response = f":{current_len}\r\n"
        
        elif commandName == "lrange":

            key = requestParams[0]
            start = int(requestParams[1])
            stop = int(requestParams[2])
            items = get_items(key, start, stop)
            response = f"*{len(items)}\r\n"
            for item in items:
                response += formBulkString(item)

        elif commandName == "llen":

            value = get_key(requestParams[0])
            if (value == None or not isinstance(value, list)):
                _length = 0
            else:
                _length = len(value)
            response = f":{_length}\r\n"

        elif commandName == "lpop":

            key = requestParams[0]
            numElements = 1 if (len(requestParams) == 1) else int(requestParams[1])
            itemsRemoved = remove_items(key, numElements)
            if (numElements == 1 and len(itemsRemoved) == 1):
                response = formBulkString(itemsRemoved[0])
            elif(len(itemsRemoved) > 1):
                response = f"*{len(items)}\r\n"
                for item in itemsRemoved:
                    response += formBulkString(item)
            else:
                response = "$-1\r\n"

             
        
        elif commandName == "set":

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


        
        else:
            pass

        responseBytes = response.encode()
        conn.sendall(responseBytes)

    conn.close()




if __name__ == "__main__":
    main()
