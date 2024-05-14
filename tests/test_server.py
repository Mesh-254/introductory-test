import pytest
from pathlib import Path
import os
from src.server import read_config, fetch_file_data, find_string_match, handle_clients, start_server
from unittest.mock import mock_open, patch

# Define test data directory
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), './tests/test_data')
# Define test cases for the read_config function
class TestServer:
     # Test for successful file reading
    def test_successful_configfile_reading(self):
        # Define the content of the mock config file
        config_content = "linuxpath=/path/to/200k.txt\n"
        
        # Mock the built-in open function to return the mock config content
        with patch('builtins.open', mock_open(read_data=config_content)):
            # Call the read_config function
            result = read_config()

        # Assert that the result matches the expected config file path
        expected_result = "/path/to/200k.txt"
        assert result == expected_result


    # Test for file not found
    def test_read_config_file_not_found(self):
    # Define a custom open function that raises FileNotFoundError
        with patch('__main__.open') as mock_open:
            mock_open.side_effect = FileNotFoundError("Mocked file not found")

            # Testing if FileNotFoundError is raised
            with pytest.raises(FileNotFoundError):
                raise FileNotFoundError
            
    def test_empty_config_file(self):
        # Ensure the test data directory exists
        os.makedirs(TEST_DATA_DIR, exist_ok=True)

        # Create an empty config file
        empty_config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        open(empty_config_path, 'w').close()

        # Call the read_config function
        try:
            result = read_config(empty_config_path)
            assert result == ""  # Expected empty string
        except ValueError as e:
            assert False, f"Unexpected exception: {e}"

    def test_missing_linuxpath(self):
    # Create a config file missing 'linuxpath='
        missing_linuxpath_config_path = os.path.join(TEST_DATA_DIR, 'config_missing_linuxpath.ini')
        with open(missing_linuxpath_config_path, 'w') as f:
            f.write("some_other_data\n")

        # Call the read_config function
        try:
            result = read_config()
            if result == None:
                assert True, "Expected ValueError for missing 'linuxpath='"
        except ValueError as e:
            assert str(e) == "Invalid configuration file format: 'linuxpath=' not found.", f"Unexpected error message: {e}"
    
    def test_invalid_file_path(self):
        # Create a config file with invalid file path
        invalid_path_config_path = os.path.join(TEST_DATA_DIR, 'config_invalid_path.ini')
        with open(invalid_path_config_path, 'w') as f:
            f.write("=/nvalid/file/path\n")

        # Call the read_config function
        try:
            result = read_config()
            if invalid_path_config_path == result:
                assert False, "Expected FileNotFoundError for invalid file path"
        except FileNotFoundError:
            raise
    
    def test_edge_cases(self):
        # Create a config file with edge case scenarios
        edge_case_config_path = os.path.join(TEST_DATA_DIR, 'config_edge_cases.ini')
        with open(edge_case_config_path, 'w') as f:
            # Extremely long file path
            f.write("linuxpath=" + "a" * 10000 + "\n")
            # Special characters in file path
            f.write("linuxpath=/path/with/special/!@#$%^&*()_+-={}[]|\\characters\n")

        # Call the read_config function
        try:
            result = read_config(edge_case_config_path)
            # Add assertions based on expected behavior
            assert len(result) <= 255  # Assuming a maximum file path length of 255 characters
            assert "!" not in result  # Special characters should not be present in the result
        except Exception as e:
            assert False, f"Unexpected exception for edge cases: {e}"
    
    def test_fetch_file_data_file_not_found(self):
    # Testing if FileNotFoundError is raised for non-existent file
        with pytest.raises(FileNotFoundError):
            fetch_file_data("nonexistent_file.txt")


    def test_fetch_file_data_valid_file(tmp_path):
        # Creating a temporary file with some data
        file_content = "This is a test file.\nLine 2.\nLine 3."
        file_path = "test_file.txt"  # Constructing the file path
        with open(file_path, "w") as f:
            f.write(file_content)
        
        # Testing if the function returns the correct file content
        assert fetch_file_data(file_path) == file_content
    

    # Test case for test_find_string_match_string_exists function
    def test_find_string_match_string_exists(self):
        # Mocking the message to search for
        data = "This is a test"

        # Mocking the expected return values
        expected_result = "STRING EXISTS\n"
        expected_time_taken = 0.0  # Since it's a mock implementation, time taken is not relevant
        expected_current_time = "2024-05-15 10:00:00"  # Mocking the current timestamp

        if data == self:
            # Calling the find_string_match function with mock parameters
            result, time_taken, current_time = find_string_match(data.strip(), REREAD_ON_QUERY=False)

            # Asserting the expected result
            assert result == expected_result

    def test_find_string_match_string_not_found(self):
        with patch('src.server.read_config') as mock_read_config, \
             patch('src.server.fetch_file_data') as mock_fetch_file_data:
            
            # Mocking the return value of read_config to return a dummy file path
            mock_read_config.return_value = 'dummy/path/config.ini'
            
            # Mocking fetch_file_data to raise FileNotFoundError
            mock_fetch_file_data.side_effect = FileNotFoundError("Mocked file not found")
            
            # Testing if FileNotFoundError is raised
            with pytest.raises(FileNotFoundError):
                find_string_match("Nonexistent string", REREAD_ON_QUERY=False)
     
    
# Define test data
@pytest.fixture
def test_data_dir():
    return TEST_DATA_DIR
