from socket import *
import threading
import time
import os
import select

HEADER = 64
PORT = 5050
SERVER = gethostbyname(gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
server.settimeout(30)

#def handle_client(conn, addr):
#    print(f"[NEW CONNECTION] {addr} connected.")
#
#    connected = True
#    while connected:
#        msg_length = conn.recv(HEADER).decode(FORMAT)
#        if msg_length:
#            msg_length = int(msg_length)
#            msg = conn.recv(msg_length).decode(FORMAT)
#            if msg == DISCONNECT_MESSAGE:
#                connected = False
#
#            print(f"[{addr}] {msg}")
#            conn.send("Msg received".encode(FORMAT))
#
#    conn.close()
#

def start():
    TIMEOUT = 15.0
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:

        ready = select.select([server], [], [], TIMEOUT)
        if ready[0] == []: #Timeout
            response = 'HTTP/1.1 408 REQUEST TIME OUT'
            print(response)
            server.sendall(response.encode())
            server.close()
            break
        
        conn, addr = server.accept()

        request = conn.recv(1024).decode()

        print(request)
        
        # Parse HTTP headers
        headers = request.split('\n')
        filename = headers[0].split()[1]

        # validRequest(SERVER + ":" + str(PORT) + "/" + filename)

        # Get the content of the file
        if filename == '/test.html':
            filename = 'test.html'

        try:
            fin = open(filename)
            content = fin.read()
            fin.close()

            response = 'HTTP/1.1 200 OK\n\n' + content
            print(response)

        except FileNotFoundError:
            response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
            print (response)
        
        conn.sendall(response.encode())
        conn.close()
        
#        thread = threading.Thread(target=handle_client, args=(conn, addr))
#        thread.start()
#        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
