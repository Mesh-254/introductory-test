#!/usr/bin/env python3
import socket
import ssl

FORMAT = 'UTF-8'
HEADERSIZE = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())


# SSL configuration
USE_SSL = True  # Set to False to disable SSL (for testing)
SSL_CAFILE = './ssl_certs/ca_cert.pem'


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER, PORT))


# Wrap client socket with SSL if enabled
# if USE_SSL:
#     ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
#     ssl_context.load_verify_locations(SSL_CAFILE)
#     ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname=SERVER)
# else:
#     ssl_socket = client_socket

# print(ssl_socket)


def send_search_query(search_query: str) -> None:
    """
    Sends a search query to the server.

    Args:
        search_query (str): The search query to send.

    Returns:
        None
    """

    search_query_length = len(search_query)
    send_length = str(search_query_length).encode(FORMAT).strip()
    send_length += b'\n' * (HEADERSIZE - len(send_length))
    client_socket.send(send_length)
    client_socket.send(search_query.encode(FORMAT))


def receive_message() -> str:
    """
    Receives a message from the server.



    Returns:
        str: The received message.
    """

    message_header = client_socket.recv(HEADERSIZE).decode(FORMAT)
    if not message_header:
        print(f"Client {client_socket} disconnected")

    try:
        message_length = int(message_header.strip())

    except ValueError:
        print(f"Invalid message header: {message_header}")

    finally:
        message = client_socket.recv(message_length).decode(FORMAT)
        return f'[Received message from server] {message_length} : {message}'


def main() -> None:
    """
    Main function to continuously accept user
    input and send messages to the server.
    """
    # Continuously accept user input and send messages to the server
    while True:
        search_text = input("Enter your message ('exit' to quit): ")
        if search_text.lower() == 'exit':
            break
        send_search_query(search_text)
        response = receive_message()
        print(response)


if __name__ == '__main__':
    main()
