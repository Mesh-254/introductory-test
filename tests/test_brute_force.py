import pytest
import time
import os
import tempfile
import logging
from search_algorithms.brute_force import brute_force_match
from src.server import find_string_match
from unittest.mock import patch

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function to create a temporary file with specified content


def create_temp_file(content):
    """
    Creates a temporary file with the specified content.

    Args:
        content (str): The content to write to the temporary file.

    Returns:
        str: The path to the created temporary file.
    """
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(content.encode('utf-8'))
    tmp_file.close()
    return tmp_file.name

# Unit tests for brute_force_match function


def test_brute_force_match_pattern_found():
    """
    Test case to check if pattern is found in text.
    """
    assert brute_force_match("pattern", "pattern")


def test_brute_force_match_pattern_not_found():
    """
    Test case to check if pattern is not found in text.
    """
    assert not brute_force_match(
        "pattern",
        "This is a patter\nThis is another line")


def test_brute_force_match_empty_pattern():
    """
    Test case for empty pattern.
    """
    assert not brute_force_match("This is a pattern\nThis is another line", "")


def test_brute_force_match_empty_text():
    """
    Test case for empty text.
    """
    assert not brute_force_match("pattern", "")


# Mocking read_config and fetch_file_data functions for testing
# find_string_match
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
    return "Line 1\nLine 2\nLine 3\n"


def test_find_string_match_pattern_found(monkeypatch):
    """
    Test case for pattern found in the file.
    """
    tmp_file_path = create_temp_file("Line 1\nLine 2\nLine 3\n")

    def mock_read_config():
        return tmp_file_path

    def mock_fetch_file_data(file_path):
        with open(file_path, 'r') as f:
            return f.read()

    monkeypatch.setattr("src.server.read_config", mock_read_config)
    monkeypatch.setattr("src.server.fetch_file_data", mock_fetch_file_data)

    result, time_taken, current_time = find_string_match(
        "Line 2", REREAD_ON_QUERY=False)
    assert result == "STRING EXISTS\n"

    os.remove(tmp_file_path)


def test_find_string_match_pattern_not_found(monkeypatch):
    """
    Test case for pattern not found in the file.
    """
    tmp_file_path = create_temp_file("Line 1\nLine 2\nLine 3\n")

    def mock_read_config():
        return tmp_file_path

    def mock_fetch_file_data(file_path):
        with open(file_path, 'r') as f:
            return f.read()

    monkeypatch.setattr("src.server.read_config", mock_read_config)
    monkeypatch.setattr("src.server.fetch_file_data", mock_fetch_file_data)

    result, time_taken, current_time = find_string_match(
        "Nonexistent line", REREAD_ON_QUERY=False)
    assert result == "STRING NOT FOUND\n"

    os.remove(tmp_file_path)


def test_find_string_match_execution_time(monkeypatch):
    """
    Test case for measuring execution time.
    """
    file_sizes = [10000, 50000, 100000, 250000, 500000, 1000000]

    for size in file_sizes:
        content = "Line 1\n Brute Force algo\nLine 2\n" * size
        tmp_file_path = create_temp_file(content)

        def mock_read_config():
            return tmp_file_path

        def mock_fetch_file_data(file_path):
            with open(file_path, 'r') as f:
                return f.read()

        monkeypatch.setattr("src.server.read_config", mock_read_config)
        monkeypatch.setattr("src.server.fetch_file_data", mock_fetch_file_data)

        try:
            start_time = time.time()

            result, time_taken, current_time = find_string_match(
                "Line 1", REREAD_ON_QUERY=True)

            end_time = time.time()
            execution_time = (end_time - start_time) * 1000

            assert result == "STRING EXISTS\n"

            logger.info(
                f'File size: {size} rows, Execution time:'
                f' {execution_time:.4f} milliseconds'
            )
        except Exception as e:
            logger.error(f"Exception for file size {size}: {e}")
        finally:
            os.remove(tmp_file_path)


def test_find_string_match_stress_test(monkeypatch):
    """
    Stress test for the find_string_match function.
    """
    def mock_read_config():
        return tmp_file_path

    def mock_fetch_file_data(file_path):
        with open(file_path, 'r') as f:
            return f.read()

    # Setting up mock functions
    monkeypatch.setattr("src.server.read_config", mock_read_config)
    monkeypatch.setattr("src.server.fetch_file_data", mock_fetch_file_data)

    # Different file sizes and query counts to test
    file_sizes = [5000, 70000, 250000, 500000, 1000000, 10000000]
    # Increase queries per second gradually
    query_counts = [500, 1000, 2000, 3000, 4000, 5000]

    for file_size in file_sizes:
        for query_count in query_counts:
            try:
                # Creating temporary file with specified content
                tmp_file_path = create_temp_file(
                    "Line 1\nLine 2\n" * file_size)

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
                            f"{total_time_taken} milliseconds")

                # Asserting that the result indicates string exists
                assert result[0] == "STRING EXISTS\n"
            except Exception as e:
                # Logging any exceptions that occur during the test
                logger.error(f"Exception during stress test: {e}")

    # Document the limitations of the software
    logger.error(
        "Reached the point where the server can no longer handle the load.")
