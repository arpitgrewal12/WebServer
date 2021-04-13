import socket
import time


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


clientSocket.connect((SERVER, PORT))

# Recieve user input from keyboard
sentence = input('Input lowercase sentence:')

# puts client to sleep 
# mimics 408 REQUEST TIME OUT 
# remove/comment out when testing other codes
time.sleep(16)

clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recv(1024)

print ('From Server:', modifiedSentence.decode())

# Close the socket
clientSocket.close()
