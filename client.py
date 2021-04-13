import socket
import time


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


clientSocket.connect((SERVER, PORT))

# Receive user input from keyboard
sentence = input('Input filename:')

# puts client to sleep 
# mimics 408 REQUEST TIME OUT 
# remove when testing other codes
# time.sleep(16)

clientSocket.send(sentence.encode())

try:
    modifiedSentence = clientSocket.recv(1024)
    print ('From Server:', modifiedSentence.decode())

except ConnectionAbortedError:
    response = 'From Server: HTTP/1.1 408 REQUEST TIME OUT \n Connection: close'
    print(response)

# Close the socket
clientSocket.close()
