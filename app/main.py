import socket  # noqa: F401
import threading
from .streams.stream_commands import *
from .respParser import parser
from .commands import *
from .array_commands import *

def command_handler(commandName):

    commands = {
        "ping" : Ping,
        "echo" : Echo,
        "get" : Get,
        "rpush" : Rpush,
        "lpush" : Lpush,
        "lpop" : Lpop,
        "blpop" : Blpop,
        "lrange" : Lrange,
        "llen" : Llen,
        "set" : Set,
        "type" : Type,
        "xadd" : Xadd
    }
    return commands[commandName]

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

        if request is None:
            break

        (commandName, requestParams) = parser(request)

        commandHandler = command_handler(commandName)
        response = commandHandler(requestParams) 
        responseBytes = response.encode()
        conn.sendall(responseBytes)

    conn.close()




if __name__ == "__main__":
    main()
