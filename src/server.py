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
import os
import signal

FORMAT = 'UTF-8'  # Setting the encoding format for communication
HEADERSIZE = 1024  # Setting the header size for messages
PORT = 44445  # Setting the port number for the server
# Getting the server IP address
# SERVER = '192.168.0.102'

SERVER = socket.gethostbyname(socket.gethostname())


# SSL configuration
USE_SSL = True  # Set to False to disable SSL (for testing)
SSL_CERTFILE = './ssl_certs/server.crt'
SSL_KEYFILE = './ssl_certs/private.key'


def read_config(config_file_path=None) -> str:
    """
    Reads the configuration file to get the path.

    Returns:
        str: The file path specified in the configuration.
    Raises:
        FileNotFoundError: If the configuration file is not found.
    """

    # If no config file path is provided,
    # use the default config.ini file located in
    # the same directory as the current script
    if config_file_path is None:
        config_file_path = os.path.join(
            os.path.dirname(__file__), 'config.ini')

    try:
        with open('config.ini', 'r') as f:
            for data in f:
                if data.startswith('linuxpath='):
                    file_path = data.strip().split('=')[1].strip()
                    return file_path

    except FileNotFoundError as e:
        # Log the error message to stderr
        sys.stderr.write(f"Error accessing config file: {e}\n")
        # Re-raise the exception to propagate it further
        raise FileNotFoundError("Config file not found")

    # Return an empty string if the file is empty or the key is not found
    return ""


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
        raise
    except Exception as e:  # Handling other exceptions
        sys.stderr.write(
            "An error occurred while reading the file: {}\n".format(
                str(e)))
        raise


def brute_force_match(pattern: str, text: str) -> bool:
    """
    Performs brute-force string matching to check if pattern matches text line.

    Args:
        pattern (str): The pattern to search for.
        text (str): The text to search in.

    Returns:
        bool: True if pattern matches a line in text, False otherwise.
    """
    m = len(pattern)  # Length of the pattern
    n = len(text)  # Length of the text

    # If the length of the pattern is greater than the length of the text,
    # there can be no match
    if m > n:
        return False  # No match if pattern is longer than text

    # Iterate through each line in the text
    for line in text.splitlines():
        # Check if the current line matches the pattern
        if line == pattern:
            return True  # Match found

    return False  # No match found


file_data = None  # Define a global variable to store file contents


def find_string_match(
        message: str, REREAD_ON_QUERY: bool = False) -> Tuple[str, float, str]:
    """
    Searches for a full match of a string in a file.

    Args:
        message (str): The string to search for.
        REREAD_ON_QUERY (bool): Whether to re-read the file on every query.

    Returns:
        tuple: A tuple containing the search result
        ('STRING EXISTS\n' or 'STRING NOT FOUND\n'),
        time taken to find the match, and the current timestamp.
    """

    global file_data  # Declare file_data as a global variable

    file_path = read_config()  # Getting the file path from configuration

    # Re-read the file on every query or if file_data is not present
    if REREAD_ON_QUERY or file_data is None:
        file_data = fetch_file_data(file_path)  # Fetch the file data

    start_time = time.time()  # Recording the start time of search

    # Split the message into lines to match against the file data
    pattern_lines = message.splitlines()
    text_lines = file_data.splitlines()  # Split the file data into lines

    # Iterate through each line in the file data
    for line in text_lines:
        # Check if the current line matches the message using brute force
        if brute_force_match(line, message):
            end_time = time.time()  # Recording the end time
            time_taken = end_time - start_time  # Calculating the time taken
            current_time = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime())  # Getting the current timestamp
            # Returning match result, time taken, and timestamp
            return 'STRING EXISTS\n', time_taken, current_time

    end_time = time.time()  # Recording the end time
    time_taken = end_time - start_time  # Calculating the time taken
    current_time = time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.localtime())  # Getting the current timestamp
    # Returning match result, time taken, and timestamp
    return 'STRING NOT FOUND\n', time_taken, current_time


def handle_clients(client_socket: socket.socket,
                   address: Tuple[str, int]) -> None:
    """
    Handles client connections and communication.

    Args:
        client_socket (socket.socket): The client socket.
        address (tuple): The address of the client.

    Returns:
        None
    """
    try:
        # Printing client connection info
        sys.stdout.write(f'Server established new connection from {
            address}\n')
        sys.stdout.flush()

        # Wrap client socket with SSL if enabled
        # if USE_SSL:
        #     context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        #     context.load_cert_chain(SSL_CERTFILE, SSL_KEYFILE)
        #     ssl_socket: Union[socket.socket, ssl.SSLSocket] =
        #     context.wrap_socket(client_socket, server_side=True)
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

            # Checking if header is empty or has zero length
            if not message_header or not len(message_header):
                # Printing client disconnection info
                sys.stdout.write(f"Client {address} disconnected\n")
                sys.stdout.flush()
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

            sys.stdout.write('"DEBUG"\n')
            sys.stdout.flush()

            # Printing received message from client
            sys.stdout.write(f'[Received string from Client {
                address}:] Length {message_length} : {message}\n')
            # Flush the output to ensure it's immediately written to the file
            sys.stdout.flush()
            # r Search for the match in the file using the received search
            # query
            string_match, time_taken, current_time = find_string_match(
                message)  # Searching for string match
            if string_match:  # Checking if string match is found
                sys.stdout.write(string_match)  # Printing string match
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

                # Printing current timestamp
                sys.stdout.write(current_time + '\n')
                # Flush the output to ensure it's immediately written to the
                # file
                sys.stdout.flush()

            if string_match:
                try:
                    # Code to send the string match to client
                    # Getting length of string match
                    string_length = len(string_match)
                    send_length = str(string_length).encode(
                        FORMAT)  # Encoding string length
                    # Padding the header size
                    send_length += b'\n' * (HEADERSIZE - len(send_length))
                    # Sending header length to client
                    client_socket.send(send_length)
                    # Sending string match to client
                    client_socket.send(string_match.encode(FORMAT))

                except Exception as e:
                    sys.stderr.write(
                        f'Error occured while sending string match{e}')

    except Exception as e:  # Handling exceptions
        # Printing error message
        sys.stderr.write(f"Error handling client {address} request: {e}\n")


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

        try:
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
        except Exception as e:
            sys.stderr.write(f"Error accepting client connection{e}")
            sys.exit()


if __name__ == '__main__':

    start_server()  # Starting the server
