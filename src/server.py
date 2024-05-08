import socket
import time
import pickle


HEADERSIZE = 10



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Create a socket object with ip address and TCP
s.bind((socket.gethostname(), 1234)) # Bind to a free port using a tuple  of (host, port).
s.listen(5)     # Now wait for  client connection. The number specifies how many clients can queue up at once

while True:
    clientsocket, address = s.accept()
    print(f"connection from {address} established !")
    msg = 'Welcome to server!'
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    clientsocket.send(bytes(msg, 'utf-8'))# Send a welcome message to connected client


    while True:
        time.sleep(2)
        msg = f'Waiting for data... at this time {time.time()}'
        msg = f'{len(msg):< {HEADERSIZE}}' + msg
        clientsocket.send(bytes(msg,'utf-8')) # Send current time 
        
    
