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


def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

#timestamp
def never_stop():
    time_started = time.time()
    X = 20
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

x= None
def handle_client(conn, addr):
    
    TIMEOUT = 60.0
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        print('The message got from client socket:', conn)
        
        
        request = conn.recv(1024).decode()
    

        headers = request.split('\n')
        file = headers[0].split()[1]
        method = headers[0].split()[0]
        
        
        # Get the content of the file
        if (file == '/'  or file == '/test.html'):
            file = 'test.html'
            
            
        if (method != "GET"):
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"
            conn.send(bytes(response, encoding='utf8'))
            print(response)
            conn.close()
            break
#            print(file)
        try:
             #            file='/Users/arpitkaur/Desktop/Webserver'+filename
            ready = select.select([conn], [], [], TIMEOUT)
            print(ready)
            if ready[0] == []: #Timeout
                response = 'HTTP/1.1 408 REQUEST TIME OUT'
                print(response)

                break

            f = open(file)
            content = f.read()
            t1 = threading.Thread(target=never_stop, args=(2,))
            f.close()
            
            print("Last modified: ", modification_date(file))
            print("Date created:", created_date(file))
            print("Last access Time:", last_accessed(file))

            last_modified=to_integer(modification_date(file))
            date_created = created_date(file)
            accessed = last_accessed(file)
            
    
            if request.__contains__('<body>') or request.__contains__('</body>'):
                return 'HTTP/1.1 400 BAD REQUEST\n\n'
                conn.close()
            
            
            global x
            if(x):
            # print("x:",x)
                if(last_modified < x):
                    response = 'HTTP/1.1 304 NOT MODIFIED \n\n' + content
                    print(response)
                    conn.send(bytes(response,encoding=FORMAT))
                    conn.send(bytes('304 Not Modified', encoding=FORMAT))
                    conn.close()
                            
            else:
                x=int(round(time.time()))
            #   print("x:",x)
                response = 'HTTP/1.1 200 OK \n\n' + content
                print(response)
                conn.send(bytes(response,encoding=FORMAT))
                conn.close()

        except FileNotFoundError:
            response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
            print(response)
            conn.send(bytes(response,encoding=FORMAT))
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
        conn.send(bytes('CONNECT_SUCCESSFUL',encoding='utf8'))
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print("[STARTING] server is starting...")
start()


