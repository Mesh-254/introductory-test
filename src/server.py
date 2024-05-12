#!/usr/bin/env python3

# Importing the socket module for network communication
import socket
# Importing threading for handling multiple client connections
import threading
# Importing sys for system operations
import sys
import time  # Importing time for time-related operations
import ssl  # Importing ssl for secure socket layer operations
from typing import Tuple, List  # Importing typing for type hints

FORMAT = 'UTF-8'  # Setting the encoding format for communication
HEADERSIZE = 1024  # Setting the header size for messages
PORT = 5050  # Setting the port number for the server
# Getting the server IP address
SERVER = '192.168.0.102'

# SERVER = socket.gethostbyname(socket.gethostname())


# SSL configuration
# USE_SSL = True  # Set to False to disable SSL (for testing)
# SSL_CERTFILE = './ssl_certs/certchain.pem'
# SSL_KEYFILE = './ssl_certs/private.key'


def read_config() -> str:
    """
    Reads the configuration file to get the path.

    Returns:
        str: The file path specified in the configuration.
    Raises:
        FileNotFoundError: If the configuration file is not found.
    """
    try:
        with open('/home/frosty/projects/introductory-test/config.ini',
                  'r') as f:
            # Iterating through the lines in the configuration file
            for data in f:
                if data.startswith(
                        'linuxpath='):  # Checking for the linuxpath line
                    file_path = data.strip().split(
                        '=')[1]  # Extracting the file path
                    return file_path  # Returning the file path

    except FileNotFoundError as e:  # Handling file not found error
        sys.stderr.write("Error accessing config file : {}\n".format(str(e)))
        sys.exit()  # Exiting the program if config file is not found


def fetch_file_data(file_path: str) -> str:
    """
    Reads and fetches contents from the specified file path.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The contents of the file.
    Raises:
        FileNotFoundError: If the specified file is not found.
        Exception: If an error occurs while reading the file.
    """
    try:
        with open(file_path, 'r') as f:  # Opening the file in read mode
            file_data = f.read()  # Reading the contents of the file
            return file_data  # Returning the file data
    except FileNotFoundError as e:  # Handling file not found error
        sys.stderr.write("file in path was not found: {}\n".format(str(e)))
        sys.exit()  # Exiting the program if file is not found
    except Exception as e:  # Handling other exceptions
        sys.stderr.write(
            "An error occurred while reading the file: {}\n".format(
                str(e)))
        sys.exit()  # Exiting the program if an error occurs


def find_string_match(
        message: str, REREAD_ON_QUERY: bool = True) -> Tuple[str, float, str]:
    """
    Searches for a full match of a string in a file.

    Args:
        message (str): The string to search for.
        REREAD_ON_QUERY (bool): Whether to re-read the file on every query.

    Returns:
        tuple: A tuple containing the search result,
        time taken to find the match,
               and the current timestamp.
    """
    file_path = read_config()  # Getting the file path from configuration

    if REREAD_ON_QUERY:
        # Get file content and store it in memory
        file_data = fetch_file_data(file_path)  # Fetching file data
    else:
        # Use global variable which contains data from last search
        if 'file_data' not in globals():
            # Fetching file data if not already present
            file_data = fetch_file_data(file_path)
        file_data = file_data  # Storing file data

    start_time = time.time()  # Recording the start time of search

    # Perform KMP string search for each line in the file
    for line in file_data.splitlines():

        if message.strip() in line:
            end_time = time.time()  # Recording the end time
            time_taken = end_time - start_time  # Calculating the time taken
            current_time = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime())  # Getting current timestamp
            # Returning match result, time taken, and timestamp
            return 'STRING EXISTS\n', time_taken, current_time

    end_time = time.time()  # Recording the end time
    time_taken = end_time - start_time  # Calculating the time taken
    current_time = time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.localtime())  # Getting current timestamp
    # Returning match result, time taken, and timestamp
    return 'STRING NOT FOUND\n', time_taken, current_time


def handle_clients(client_socket: socket.socket, address: tuple) -> None:
    """
    Handles client connections and communication.

    Args:
        client_socket (socket.socket): The client socket.
        address (tuple): The address of the client.

    Returns:
        None
    """
    try:
        sys.stdout.write(f'Server established new connection from {
                         address}\n')  # Printing client connection info

        # Wrap client socket with SSL if enabled
        # if USE_SSL:
        #     context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        #     context.load_cert_chain(SSL_CERTFILE, SSL_KEYFILE)
        #     ssl_socket = context.wrap_socket(client_socket, server_side=True)
        # else:
        #     ssl_socket = client_socket

        # Send linux path to client for config file
        path = read_config()  # Getting file path from configuration
        if path is None:
            # Raising error if file path is not found
            raise ValueError("File Path not found.")
        sys.stdout.write(f'This is the path contained in config file: {
                         path}\n')  # Printing file path

        connected = True  # Flag to indicate client connection status
        while connected:
            # Read data from client
            message_header = client_socket.recv(HEADERSIZE).decode(
                FORMAT)  # Receiving message header from client
            if not len(message_header):  # Checking if header length is zero
                return False  # Returning if header length is zero
            if not message_header:  # Checking if header is empty
                # Printing client disconnection info
                sys.stdout.write(f"Client {address} disconnected\n")
                break  # Breaking the loop if client disconnects
            try:
                # Converting message header to integer
                message_length = int(message_header.strip())
            except ValueError:
                # Handling invalid message header
                sys.stderr.write(f"Invalid message header from {
                                 address}:{message_header}\n")
                # Continuing to next iteration if message header is invalid
                continue
            # Receiving message from client
            message = client_socket.recv(message_length).decode(
                FORMAT)
            # Printing received message from client
            sys.stdout.write(f'[Received string from Client {address}:]{
                             message_length} : {message}\n')
            # Flush the output to ensure it's immediately written to the file
            sys.stdout.flush()
            # Search for the match in the file using the received search query
            string_match, time_taken, current_time = find_string_match(
                message)  # Searching for string match
            if string_match:  # Checking if string match is found
                sys.stdout.write(string_match)  # Printing string match
                # Flush the output to ensure it's immediately written to the
                # file
                sys.stdout.flush()

                # Printing current timestamp
                sys.stdout.write(current_time + '\n')
                # Flush the output to ensure it's immediately written to the
                # file
                sys.stdout.flush()

                # If time taken is less than 1 second, consider it as
                # milliseconds
                if time_taken < 1:
                    # Converting time to milliseconds
                    time_taken_ms = time_taken * 1000
                    # Printing time taken in milliseconds
                    sys.stdout.write(
                        f'Execution time: {time_taken_ms} milliseconds\n')
                    # Flush the output to ensure it's immediately written to
                    # the file
                    sys.stdout.flush()

                else:
                    # Printing time taken in seconds
                    sys.stdout.write(f'Time taken: {time_taken} seconds\n')
                    # Flush the output to ensure it's immediately written to
                    # the file
                    sys.stdout.flush()

            # Code to send the string match to client
            string_length = len(string_match)  # Getting length of string match
            send_length = str(string_length).encode(
                FORMAT)  # Encoding string length
            # Padding the header size
            send_length += b'\n' * (HEADERSIZE - len(send_length))
            client_socket.send(send_length)  # Sending header length to client
            # Sending string match to client
            client_socket.send(string_match.encode(FORMAT))

    except Exception as e:  # Handling exceptions
        # Printing error message
        sys.stderr.write(f"Error handling client {address}: {e}\n")
        sys.exit()  # Exiting the program


def start_server() -> None:
    """
    Starts the server and listens for client connections.

    Returns:
        None
    """
    server_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)  # Creating server socket
    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1)  # Setting socket options to Reload/reatart always
    server_socket.bind((SERVER, PORT))  # Binding server to address and port
    server_socket.listen()  # Starting to listen for connections
    # Printing server listening info
    sys.stdout.write(f'Server is listening at {SERVER}\n')
    sys.stdout.flush()
    while True:  # Infinite loop to accept client connections
        # Accepting client connection
        client_socket, address = server_socket.accept()

        # Start a new thread to handle the client
        # Passing target function and arguments
        thread = threading.Thread(
            target=handle_clients, args=(
                client_socket, address))
        thread.start()  # Starting the thread
        # Printing active connections count
        sys.stdout.write(
            f'[active connections:]{
                threading.active_count() - 1}\n')
        # Flush the output to ensure it's immediately written to the file
        sys.stdout.flush()


if __name__ == '__main__':

    start_server()  # Starting the server
