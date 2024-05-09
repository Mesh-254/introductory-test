import socket


FORMAT = 'UTF-8'
HEADERSIZE = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER, PORT))

def  send_search_query(search_query):
    search_query_length = len(search_query)
    send_length = str(search_query_length).encode(FORMAT)
    send_length += b'\n' * (HEADERSIZE - len(send_length))
    client_socket.send(send_length)
    client_socket.send(search_query.encode(FORMAT))

def receive_message(client_socket):
    message_header = client_socket.recv(HEADERSIZE).decode(FORMAT)
    if not message_header:
        print(f"Client disconnected")
        return False
    try:
        message_length = int(message_header.strip())
    except ValueError:
        print(f"Invalid message header from :{message_header}")
        
    message = client_socket.recv(message_length).decode(FORMAT)
    print(f'[Received message:] {message_length} : {message}')
    
# Continuously accept user input and send messages to the server
while True:
    search_text = input("Enter your message ('exit' to quit): ")
    if search_text.lower() == 'exit':
        break
    send_search_query(search_text)
    response = receive_message(client_socket)
    print(response)

