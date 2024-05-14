import pytest
from src import server
from src.server import read_config, start_server, handle_clients
from unittest.mock import patch, MagicMock

import pytest
from unittest.mock import patch, MagicMock
from src import server

def test_handle_clients_successful():
    # Mocking necessary components
    client_socket = MagicMock()
    address = ('127.0.0.1', 12345)
    with patch('src.server.read_config', return_value='/path/to/config'):
        with patch('src.server.find_string_match', return_value=('match', 0.5, '2024-05-14')):
            with patch('sys.stdout.write') as mock_stdout_write:
                with patch.object(client_socket, 'send') as mock_send:
                    # Calling the function
                    server.handle_clients(client_socket, address)

    # Assertions
    mock_stdout_write.assert_called()  # Ensure stdout writes


def test_handle_clients_invalid_message_header():
    # Mocking necessary components
    client_socket = MagicMock()
    client_socket.recv.side_effect = [b'not_an_integer']
    address = ('127.0.0.1', 12345)
    with patch('sys.stderr.write') as mock_stderr_write:
        # Calling the function
        server.handle_clients(client_socket, address)

    # Assertions
    mock_stderr_write.assert_called()  # Ensure stderr write


def test_handle_clients_exception():
    # Mocking necessary components
    client_socket = MagicMock()
    client_socket.recv.side_effect = Exception('Some error')
    address = ('127.0.0.1', 12345)
    with patch('sys.stderr.write') as mock_stderr_write:
        with patch('sys.exit') as mock_exit:
            # Calling the function
            server.handle_clients(client_socket, address)

    # Assertions
    mock_stderr_write.assert_called_once()  # Ensure stderr write
    mock_exit.assert_not_called()  # Ensure sys.exit is not called



def test_start_server_successful():
    # Mocking necessary components
    with patch('src.server.socket.socket') as mock_socket:
        with patch('src.server.threading.Thread') as mock_thread:
            with patch('sys.stdout.write'):
                # Calling the function
                try:
                    start_server()
                except SystemExit:
                    pass

    # Assertions
    mock_socket.return_value.bind.assert_called_once()  # Ensure socket.bind is called
    mock_socket.return_value.listen.assert_called_once()  # Ensure socket.listen is called
    

def test_start_server_exception():
    # Mocking necessary components
    with patch('socket.socket') as mock_socket:
        mock_socket.return_value.accept.side_effect = Exception('Some error')
        with patch('sys.stderr.write') as mock_stderr_write:
            with pytest.raises(SystemExit):
                # Calling the function
                server.start_server()

    # Assertions
    mock_stderr_write.assert_called_once()  # Ensure stderr write
