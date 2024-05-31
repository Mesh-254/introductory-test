import pytest
from unittest.mock import patch, MagicMock
from src.client import send_search_query, receive_message

# Define mock data for testing
SEARCH_QUERY = "test query"
MESSAGE = "test message"

# Mock socket object


@pytest.fixture
def mock_socket():
    return MagicMock()

# Test send_search_query function


def test_send_search_query(mock_socket):
    # Arrange
    send_length = b'10\n'
    search_query = SEARCH_QUERY.encode('UTF-8')

    # Act
    send_search_query(SEARCH_QUERY, mock_socket)

    # Assert
    mock_socket.send.assert_called()
    assert mock_socket.send.call_count == 2

    # Check the second call to client_socket.send
    mock_socket.send.assert_any_call(search_query)

#   Test receive_message function


def test_receive_message(mock_socket):
    # Arrange
    message_header = b'10\n'
    message = b'Message'
    expected_message = '[Received message from server] Length: 10 : Message'

    # Mock recv method of the socket
    mock_socket.recv.side_effect = [message_header, message]

    # Act
    received_message = receive_message(mock_socket)

    # Print received and expected messages for debugging
    print("Received Message:", received_message)
    print("Expected Message:", expected_message)

    # Assert
    assert received_message.strip() == expected_message.strip()

    # Test edge cases and error handling
    # Test receiving a message with invalid message header
    mock_socket.recv.side_effect = [b'invalid_header\n']
    with pytest.raises(Exception) as exception:
        receive_message(mock_socket)
    assert str(
        exception.value) == "Error receiving message: Invalid message header"

    # Test receiving a message with incorrect length
    mock_socket.recv.side_effect = [b'0\n']
    with pytest.raises(Exception) as exception:
        receive_message(mock_socket)
    assert str(exception.value) == "Error receiving message: "


def test_integration(mock_socket):
    # Arrange
    message_header = b'10\n'
    message = MESSAGE.encode('UTF-8')

    # Mock recv method of the socket
    mock_socket.recv.side_effect = [message_header, message]

    # Act
    send_search_query(SEARCH_QUERY, mock_socket)
    received_message = receive_message(mock_socket)

    # Assert
    assert not received_message == f'[Received message from server] 10 : {
        MESSAGE}'


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
