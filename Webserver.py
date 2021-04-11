import socket
import threading
import time
import select
from requests.exceptions import HTTPError
import requests
import os
import datetime
import os.path
import stat

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
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
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def created_date(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t)


def last_accessed(filename):
    t= os.path.getatime(filename)
    return datetime.datetime.fromtimestamp(t)
    
def start():
    TIMEOUT=15.0
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
        print(conn)
        
        
        request = conn.recv(1024).decode()
#       print(request)
        conn.settimeout(20)
        # Parse HTTP headers
        headers = request.split('\n')
        filename = headers[0].split()[1]
        print(headers)
        # Get the content of the file
        if filename == '/':
            filename = '/test.html'
        
        try:
            file='/Users/arpitkaur/Desktop/Webserver'+filename
            fin = open(file)
            content = fin.read()
            fin.close()
    
            print("Last modified: " ,modification_date(file))
            print("Date created:",created_date(file))
            print("Last access Time:", last_accessed(file))
            
            last_modified=modification_date(file)
            date_created=created_date(file)
            accessed=last_accessed(file)
            
            
            if (last_modified > accessed):
                response = 'HTTP/1.1 200 OK\n\n' + content
                print(response)
                
            else:
                response = 'HTTP/1.1 304 NOT MODIFIED\n\n' + content
                print(response)

        except FileNotFoundError:

            response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
            print(response)

        
        if response.encode()=='GET / HTTP/1.1\r\n\r\n':     # HERE WE HAVE NO HEADER AND HTTP 1.1 REQUIRES A Host HEADER
            response='HTTP/1.1 400 BAD REQUEST\n\nBad Request'
    
    
        print(response.encode())
        
        conn.sendall(response.encode())
        
        conn.close()

        


#        thread = threading.Thread(target=handle_client, args=(conn, addr))
#        thread.start()
#        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
print("[STARTING] server is starting...")
start()
