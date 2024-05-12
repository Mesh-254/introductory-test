#!/usr/bin/env python3

import socket  # Importing the socket module for network communication
import ssl  # Importing ssl for secure socket layer operations

FORMAT = 'UTF-8'  # Setting the encoding format for communication
HEADERSIZE = 1024  # Setting the header size for messages
PORT = 5050  # Setting the port number for the server
# Getting the server IP address
SERVER = socket.gethostbyname(socket.gethostname())

# SSL configuration
USE_SSL = True  # Set to False to disable SSL (for testing)
SSL_CAFILE = './ssl_certs/ca_cert.pem'  # Path to CA certificate file


client_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)  # Creating client socket
client_socket.connect((SERVER, PORT))  # Connecting to server


# Wrap client socket with SSL if enabled
# if USE_SSL:
#     ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
#     ssl_context.load_verify_locations(SSL_CAFILE)
#     ssl_socket = ssl_context.wrap_socket(client_socket,
#                                 server_hostname=SERVER)
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

    search_query_length = len(search_query)  # Getting length of search query
    send_length = str(search_query_length).encode(
        FORMAT).strip()  # Encoding length of search query
    # Padding the header size
    send_length += b'\n' * (HEADERSIZE - len(send_length))
    client_socket.send(send_length)  # Sending header length to server
    # Sending search query to server
    client_socket.send(search_query.encode(FORMAT))


def receive_message() -> str:
    """
    Receives a message from the server.

    Returns:
        str: The received message.
    """

    message_header = client_socket.recv(HEADERSIZE).decode(
        FORMAT)  # Receiving message header from server
    if not message_header:  # Checking if header is empty
        # Printing client disconnection info
        print(f"Client {client_socket} disconnected")

    try:
        # Converting message header to integer
        message_length = int(message_header.strip())

    except ValueError:
        # Printing invalid message header
        print(f"Invalid message header: {message_header}")

    finally:
        message = client_socket.recv(message_length).decode(
            FORMAT)  # Receiving message from server
        return f'[Received message from server] {message_length} : {
            message}'  # Returning received message


def main() -> None:
    """
    Main function to continuously accept user
    input and send messages to the server.
    """

    # Continuously accept user input and send messages to the server
    while True:
        # Prompting user for input
        search_text = input("Enter your message ('exit' to quit): ")
        if search_text.lower() == 'exit':  # Checking if user wants to exit
            break  # Exiting the loop if user wants to quit
        send_search_query(search_text)  # Sending search query to server
        response = receive_message()  # Receiving response from server
        print(response)  # Printing the received response


if __name__ == '__main__':
    main()  # Calling the main function if script is executed directly
