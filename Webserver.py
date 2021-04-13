import socket
import threading
import time
import select
import os
import datetime
import os.path
#import stat
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
x= None

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def never_stop():
    time_started = time.time()
    X = 2
    while True:
        if time.time() > time_started + X:
            raise TimeoutException()
        # response = 'HTTP/1.1 408 REQUEST TIME OUT'
        
        
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
    x=  None
    TIMEOUT=15.0
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    
    while True:
        
        # ready = select.select([server], [], [], TIMEOUT)
        # print(ready[0])
        # if ready[0] == []: #Timeout
        #     response = 'HTTP/1.1 408 REQUEST TIME OUT'
        #     print(response)
        #     server.sendall(response.encode())
        #     break
            
        conn, addr = server.accept()

        ready = select.select([conn], [], [], TIMEOUT)
        # print(ready[0])
        if ready[0] == []: #Timeout
            response = 'HTTP/1.1 408 REQUEST TIME OUT'
            print(response)
            print(response.encode())
            conn.sendall(response.encode())
            break

        request = conn.recv(1024).decode()

        headers = request.split('\n')
        file = headers[0].split()[1]
        method = headers[0].split()[0]
        # Get the content of the file
      
        if method != "GET":
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"
            conn.send(bytes(response, encoding='utf8'))
            print(response)
            break

        if (file == '/'  or file == '/test.html'):
            file = 'test.html'
            print(file)
        try:
            f = open(file)
            content = f.read()
            t1 = threading.Thread(target=never_stop, args=(2,))
            f.close()
   
            
            print("Last modified: " ,modification_date(file))
            print("Date created:",created_date(file))
            print("Last access Time:", last_accessed(file))
                       
            last_modified=modification_date(file)
            date_created=created_date(file)
            accessed=last_accessed(file)
            
            if request.__contains__('<body>') or request.__contains__('</body>'):
                return 'HTTP/1.1 400 BAD REQUEST\n\n'
            
            if(x):
                print("x:",x)
                if(last_modified < x):
                    response = 'HTTP/1.1 304 NOT MODIFIED \n\n' + content
                    print(response)
                
            else:
                x=int(round(time.time()))
                print("x:",x)
                response = 'HTTP/1.1 200 OK \n\n' + content
                print(response)
            
        except FileNotFoundError:
            response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
            print (response)

    
        conn.sendall(response.encode())
    conn.close()
    server.close()
        


print("[STARTING] server is starting...")
start()
