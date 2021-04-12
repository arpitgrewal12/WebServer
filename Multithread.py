import socket
import threading
import time
import select
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


#timestamp
def never_stop():
    time_started = time.time()
    X = 0.00000001
    while True:
        if time.time() > time_started + X:
            raise TimeoutException()
        response = 'HTTP/1.1 408 REQUEST TIME OUT'
    
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def created_date(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t)


def last_accessed(filename):
    t = os.path.getatime(filename)
    return datetime.datetime.fromtimestamp(t)


def handle_client(conn, addr):
    TIMEOUT = 50
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        request1 = conn.recv(1024)
        request=request1.decode()

        message = request.split('\n')
        print(message)

        method = message[0].split()[0]
        print(method)

        file = message[0].split()[1]
        
        
        # Get the content of the file
        if (file == '/'  or file == '/test.html'):
            file = 'test.html'
            print(file)
        try:
             #            file='/Users/arpitkaur/Desktop/Webserver'+filename
            f = open(file)
            content = f.read()
            f.close()
            
            print("Last modified: ", modification_date(file))
            print("Date created:", created_date(file))
            print("Last access Time:", last_accessed(file))

            last_modified = modification_date(file)
            date_created = created_date(file)
            accessed = last_accessed(file)
            
    
            if request.__contains__('<body>') or request.__contains__('</body>'):
                return 'HTTP/1.1 400 BAD REQUEST\n\n'
            
            
            
            if(accessed):
                if(last_modified < accessed):
                    response = 'HTTP/1.1 304 NOT MODIFIED \n\n' + content
                    print(response)
                
                else:
                    response = 'HTTP/1.1 200 OK \n\n' + content
                    print(response)

        except FileNotFoundError:
            response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
            print(response)
        
    conn.sendall(response.encode())
    conn.close()

#        print(response.encode())
#
#    conn.sendall(response.encode())
#
#    conn.close()



def start():

    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print("[STARTING] server is starting...")
start()

server.close()
