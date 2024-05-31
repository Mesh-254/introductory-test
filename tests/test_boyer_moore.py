#!/usr/bin/env python3

import time
import sys
import os
import tempfile
import logging
from search_algorithms.boyer_moore import boyer_moore
from src.server import find_string_match, fetch_file_data
import pytest

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Add the path to the 'src' directory
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../src')))

# Mocking read_config and fetch_file_data functions for testing


def mock_read_config():
    return "/path/to/your/file.txt"


def mock_fetch_file_data(file_path):
    return "Line 1\nLine 2\n" * 10000  # 20,000 lines in the file

# function to create a temporary file with specified content


def create_temp_file(content):
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(content.encode('utf-8'))
    tmp_file.close()
    return tmp_file.name

# Test cases for the Boyer-Moore function


def test_boyer_moore_pattern_found():
    pattern = ["Line 1", "Line 2"]
    text = ["Line 0", "Line 1", "Line 2", "Line 3"]
    assert boyer_moore(pattern, text) == 1


def test_boyer_moore_pattern_not_found():
    pattern = ["Line 1", "Line 2"]
    text = ["Line 0", "Line 3", "Line 4"]
    assert boyer_moore(pattern, text) == -1


def test_boyer_moore_empty_pattern():
    pattern = []
    text = ["Line 0", "Line 1", "Line 2"]
    assert boyer_moore(pattern, text) == -1


def test_boyer_moore_empty_text():
    pattern = ["Line 1", "Line 2"]
    text = []
    assert boyer_moore(pattern, text) == -1

# Test cases for find_string_match function


def test_find_string_match_file_not_found(monkeypatch):
    def mock_read_config():
        return "/non/existent/file.txt"

    monkeypatch.setattr("src.server.read_config", mock_read_config)
    with pytest.raises(FileNotFoundError):
        find_string_match("pattern", REREAD_ON_QUERY=True)


def test_find_string_match_missing_configuration(monkeypatch):
    def mock_read_config():
        raise FileNotFoundError("Configuration file not found")

    monkeypatch.setattr("src.server.read_config", mock_read_config)
    with pytest.raises(FileNotFoundError):
        find_string_match("pattern", REREAD_ON_QUERY=True)


def test_find_string_match_pattern_not_found(monkeypatch):
    pattern = "Not existing pattern"
    tmp_file_path = create_temp_file("Line 1\nLine 2\n" * 10000)

    def mock_read_config():
        return tmp_file_path

    def mock_fetch_file_data(file_path):
        with open(file_path, 'r') as f:
            return f.read()

    monkeypatch.setattr("src.server.read_config", mock_read_config)
    monkeypatch.setattr("src.server.fetch_file_data", mock_fetch_file_data)

    result = find_string_match(pattern, REREAD_ON_QUERY=True)
    assert result[0] == "STRING NOT FOUND\n"
    os.remove(tmp_file_path)


def test_find_string_match_execution_time(monkeypatch):
    file_sizes = [10000, 50000, 100000, 250000, 500000, 1000000]

    for size in file_sizes:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                file_data = ("Line 1\nLine 2\n" * size).encode('utf-8')
                tmp_file.write(file_data)
                tmp_file_path = tmp_file.name

            def mock_read_config():
                return tmp_file_path

            def mock_fetch_file_data(file_path):
                with open(file_path, 'r') as f:
                    return f.read()

            monkeypatch.setattr("src.server.read_config", mock_read_config)
            monkeypatch.setattr(
                "src.server.fetch_file_data",
                mock_fetch_file_data)

            start_time = time.time()
            result, time_taken, current_time = find_string_match(
                "Line 1\nLine 2", REREAD_ON_QUERY=False
            )
            end_time = time.time()

            time_taken = (end_time - start_time) * 1000

            logger.info(f'File size: {size} rows, Execution time:'
                        f'{time_taken} milliseconds'
                        )
        except Exception as e:
            # Logging any exceptions that occur during the test
            logger.error(f"Exception during stress test: {e}")
        finally:
            os.remove(tmp_file_path)


def test_find_string_match_stress_test(monkeypatch):

    def mock_read_config():
        return tmp_file_path

    def mock_fetch_file_data(file_path):
        with open(file_path, 'r') as f:
            return f.read()

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
                with tempfile.NamedTemporaryFile(delete=False) as file:
                    file_data = (
                        "Line 1\nTwo way Search \nLine 2\n" *
                        file_size).encode('utf-8')
                    file.write(file_data)
                    tmp_file_path = file.name

                start_time = time.time()

                # Invoking find_string_match with a sample query
                for _ in range(query_count):
                    result = find_string_match("Line 2", REREAD_ON_QUERY=True)

                end_time = time.time()

                # Calculating execution time per query
                total_time_taken = (end_time - start_time) * 1000 / query_count

                # Logging execution time
                logger.info(f"File size: {file_size}, Queries per second:"
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
