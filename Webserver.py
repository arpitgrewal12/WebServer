import socket
import threading
import time
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.settimeout(50)
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
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        
        request = conn.recv(1024).decode()
#        print(request)
        
        # Parse HTTP headers
        headers = request.split('\n')
        filename = headers[0].split()[1]

        # Get the content of the file
        if filename == '/':
            filename = 'test.html'

        try:
            fin = open('test.html')
            content = fin.read()
            fin.close()

            response = 'HTTP/1.1 200 OK\n\n' + content
            print(response)
            
        except FileNotFoundError:
            response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found\n'
            print (response)
        except timeout:
            print("Timeout")

       
        
        conn.sendall(response.encode())
        conn.close()
        
        
        
        
        
#        thread = threading.Thread(target=handle_client, args=(conn, addr))
#        thread.start()
#        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
