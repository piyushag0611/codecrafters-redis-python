import socket  # noqa: F401
import threading
from .respParser import parser, formBulkString
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    while(True):
        conn, _ = server_socket.accept() # wait for client
        thread = threading.Thread(target = handle_conn, args=(conn,))
        thread.start()


def handle_conn(conn):


    redisKVStore = {}

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

            value = redisKVStore.get(requestParams[0])
            if (value == None):
                response = "$-1\r\n"
            else:
                response = formBulkString(value)
        
        elif commandName == "set":

            if (len(requestParams) >= 2):
                key = requestParams[0]
                value = requestParams[1]
                redisKVStore[key] = value

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
