import socket


FORMAT = 'UTF-8'
HEADERSIZE = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER, PORT))

def  send_search_query(search_query):
    search_query_length = len(search_query)
    send_length = str(search_query_length).encode(FORMAT).strip()
    send_length += b'\n' * (HEADERSIZE - len(send_length))
    client_socket.send(send_length)
    client_socket.send(search_query.encode(FORMAT))

def receive_message():
   
    message_header = client_socket.recv(HEADERSIZE).decode(FORMAT)
    if not message_header:
        print(f"Client {client_socket} disconnected")

    try:
        message_length = int(message_header.strip())
        
    except ValueError:
        print(f"Invalid message header:{message_header}")
    
    finally:
        message = client_socket.recv(message_length).decode(FORMAT)
        return f'[Received message from server:] {message_length} : {message}'
    
# Continuously accept user input and send messages to the server
while True:
    search_text = input("Enter your message ('exit' to quit): ")
    if search_text.lower() == 'exit':
        break
    send_search_query(search_text)
    response = receive_message()
    print(response)

