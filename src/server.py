import socket
import threading
import sys
import time

FORMAT = 'UTF-8'
HEADERSIZE = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER, PORT))


# function to read the config file
def read_config():
    try:
        with open('./config.ini', 'r') as f:
            for data in f:
                if data.startswith('linuxpath='):
                    file_path = data.strip().split('=')[1]
                    return file_path
                

    except FileNotFoundError as e:
        print("Error accessing config file : ", str(e), "\n")
        sys.exit()

# function to search full match of a string contained in file 
def find_string_match(message):
    """
    Searches for a full match of a string in a file.

    Args:
        file_path (str): The path to the file to search.
        search_string (str): The string to search for.

    Returns:
        bool: True if the string is found, False otherwise AND TIME TAKEN TO find match.
    """
    file_path = read_config()
    try:
        start_time = time.time()  # Record the start time
        with open(file_path, 'r') as f:
            data = f.read()
            if message.strip() in data:

                end_time = time.time()  # Record the end time
                time_taken = end_time - start_time  # Calculate the time taken

                return 'STRING EXISTS\n', time_taken

            end_time = time.time()  # Record the end time
            time_taken = end_time - start_time  # Calculate the time taken

            return 'STRING NOT FOUND\n', time_taken
    except FileNotFoundError as e:
        print("The specified file was not found.", str(e))
        sys.exit()
    except Exception as e:
        print("An error occurred while reading the file.", str(e))
        sys.exit()

def handle_clients(client_socket, address):
    try:
        print(f'Server established new connection from {address}')
        
        # send linux path to client for config file
        path = read_config()
        if path is None:
            raise ValueError("File Path not found.")
        print(f'This is the path contained in config file: {path}')


        connected = True
        while connected:
            # Read data from client
            message_header = client_socket.recv(HEADERSIZE).decode(FORMAT)
            if not len(message_header):
                return False
            if not message_header:
                print(f"Client {address} disconnected")
                break
            try:
                message_length = int(message_header.strip())
            except ValueError:
                print(f"Invalid message header from {address}:{message_header}")
                continue
            message = client_socket.recv(message_length).decode(FORMAT)
            print(f'[Received string from Client {address}:] {message_length} : {message}')


            # Search for the match in the file using the received search query
            string_match, time_taken = find_string_match(message)
            if string_match:
                print(string_match)

                if time_taken < 1:  # If time taken is less than 1 second, consider it as milliseconds
                    time_taken_milliseconds = time_taken * 1000
                    print(f'Time taken: {time_taken_milliseconds} milliseconds')
                else:
                    print(f'Time taken: {time_taken} seconds')
            
            # Code to send the string match to client
            string_length = len(string_match)
            send_length = str(string_length).encode(FORMAT)
            send_length += b'\n' * (HEADERSIZE - len(send_length))
            client_socket.send(send_length)
            client_socket.send(string_match.encode(FORMAT))

    except Exception as e:
        print(f"Error handling client {address}: {e}")
        sys.exit()


 

def start_server():
    server_socket.listen()
    print(f'Server is listening at {SERVER}')
    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(
            target=handle_clients, args=(client_socket, address))
        thread.start()
        print(f'[active connections:]{threading.active_count() - 1}')

if __name__ == '__main__':


    start_server()
