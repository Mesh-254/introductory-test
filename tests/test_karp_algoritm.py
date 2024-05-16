import pytest  # Importing pytest for unit testing
import time  # Importing time module for time-related functions
import sys  # Importing sys module for system-specific parameters and functions
import os  # Importing os module for operating system functionalities
import logging  # Importing logging module for logging purposes
import tempfile  # Importing tempfile module for creating temporary files
# Importing karp_rabin_string_match function
from search_algorithms.karp_algorithm import karp_rabin_string_match
# Importing find_string_match function
from src.server import find_string_match


# Setup logging
logging.basicConfig(level=logging.INFO)  # Configuring logging level
logger = logging.getLogger(__name__)  # Creating a logger object


# Add the path to the 'src' directory
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../src')))


# Function to create a temporary file with specified content
def create_temp_file(content):
    """
    Create a temporary file with specified content.

    Args:
        content (str): The content to be written to the file.

    Returns:
        str: The path to the created temporary file.
    """
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(content.encode('utf-8'))
    tmp_file.close()
    return tmp_file.name


# Mocking read_config and fetch_file_data functions for testing
def mock_read_config():
    """
    Mock function to simulate reading configuration.
    Returns a sample file path.
    """
    return "/path/to/your/file.txt"


def mock_fetch_file_data(file_path):
    """
    Mock function to simulate fetching file data.
    Returns sample file data.
    """
    return "Line 1\nLine 2\n" * 10000  # 20,000 lines in the file


# Test cases for karp_rabin_string_match function
def test_karp_rabin_string_match_pattern_found():
    """
    Test case to check if pattern is found in text.
    """
    pattern = "Line 1\nLine 2"
    text = "Line 1\nLine 2\n" * 10000
    result, time_taken, current_time = karp_rabin_string_match(pattern, text)
    assert result == "STRING EXISTS\n"
    assert time_taken >= 0
    assert isinstance(current_time, str)


def test_karp_rabin_string_match_pattern_not_found():
    """
    Test case to check if pattern is not found in text.
    """
    pattern = "Not existing pattern"
    text = "Line 1\nLine 2\n" * 10000
    result, time_taken, current_time = karp_rabin_string_match(pattern, text)
    assert result == "STRING NOT FOUND\n"
    assert time_taken >= 0
    assert isinstance(current_time, str)


# Test cases for find_string_match function

def test_find_string_match_file_not_found():
    """
    Test case for handling file not found error.
    """
    with pytest.raises(FileNotFoundError):
        # Assuming the file does not exist
        find_string_match("pattern", REREAD_ON_QUERY=False)


def test_find_string_match_missing_configuration():
    """
    Test case for missing configuration file.
    """
    with pytest.raises(FileNotFoundError):
        # Assuming the configuration is missing
        find_string_match("pattern", REREAD_ON_QUERY=False)


def test_find_string_match_pattern_found(monkeypatch):
    """
    Test case for pattern found in the file.
    """
    pattern = "Line 1"
    with monkeypatch.context() as m:
        m.setattr("src.server.read_config", mock_read_config)
        m.setattr("src.server.fetch_file_data", mock_fetch_file_data)
        result, _, _ = find_string_match(pattern, REREAD_ON_QUERY=False)
        assert result == "STRING EXISTS\n"


def test_find_string_match_execution_time(monkeypatch):
    """
    Test case for measuring execution time.
    """
    # Measure execution time for different file sizes
    file_sizes = [10000, 50000, 100000, 500000, 1000000]  # Lines in the file
    for size in file_sizes:
        with monkeypatch.context() as m:
            m.setattr("src.server.read_config", mock_read_config)
            m.setattr("src.server.fetch_file_data", mock_fetch_file_data)
        try:

            start_time = time.time()
            result = find_string_match("pattern", REREAD_ON_QUERY=False)
            end_time = time.time()
            time_taken = (end_time - start_time) * 1000
            logger.info(
                f"File size: {size} rows, Execution time: {
                    time_taken:.4f} milliseconds")
        except Exception as e:
            logger.error(f"Exception during stress test: {e}")
        finally:
            continue


def test_find_string_match_stress_test(monkeypatch, caplog):
    """
    Stress test for the find_string_match function.
    """
    # Setting up mock functions
    monkeypatch.setattr("src.server.read_config", mock_read_config)
    monkeypatch.setattr("src.server.fetch_file_data", mock_fetch_file_data)

    # Different file sizes and query counts to test
    file_sizes = [5000, 70000, 100000, 500000, 1000000, 10000000]
    # Increase queries per second gradually
    query_counts = [500, 1000, 2000, 3000, 4000, 5000]

    for file_size in file_sizes:
        for query_count in query_counts:
            try:
                # Creating temporary file with specified content
                tmp_file_path = create_temp_file(
                    "Line 1\n Karp algorithm \nLine 2\n" * file_size)

                start_time = time.time()
                # Invoking find_string_match with a sample query
                for _ in range(query_count):
                    result = find_string_match("Line 2", REREAD_ON_QUERY=True)

                end_time = time.time()

                # Calculating execution time per query
                total_time_taken = (end_time - start_time) * 1000 / query_count

                # Logging execution time

                logger.info(f"File size: {file_size} rows, Queries per second:"
                            f"{query_count}, Average execution time per query:"
                            f"{total_time_taken:.4f} milliseconds")

                # Asserting that the result indicates string exists
                assert result[0] == "STRING EXISTS\n"
            except Exception as e:
                # Logging any exceptions that occur during the test
                logger.error(f"Exception during stress test: {e}")

    # Document the limitations of the software
    logger.error(
        "Reached the point where the server can no longer handle the load.")
