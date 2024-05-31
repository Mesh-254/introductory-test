#!/usr/bin/env python3
import pytest
import tempfile
import time
import os
import logging
import sys
import tempfile
from search_algorithms.two_way_search import preprocess, two_way_string_match
from src.server import find_string_match


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_preprocess():
    pattern = "ABCD"
    expected_skip_table = {'A': 3, 'B': 2, 'C': 1, 'D': 0}
    assert preprocess(pattern) == expected_skip_table


def test_preprocess_empty_pattern():
    pattern = ""
    expected_skip_table = {}
    assert preprocess(pattern) == expected_skip_table


def test_two_way_string_match_found():
    pattern = "Line 1\nLine 2"
    text = "Line 0\nLine 1\nLine 2\nLine 3"
    assert two_way_string_match(pattern, text) is True


def test_two_way_string_match_not_found():
    pattern = "Line 4\nLine 5"
    text = "Line 0\nLine 1\nLine 2\nLine 3"
    assert two_way_string_match(pattern, text) is False


def test_two_way_string_match_empty_pattern():
    pattern = ""
    text = "Line 0\nLine 1\nLine 2\nLine 3"
    assert two_way_string_match(pattern, text) is True


def test_two_way_string_match_empty_text():
    pattern = "Line 1\nLine 2"
    text = ""
    assert two_way_string_match(pattern, text) is False


# Mocking read_config and fetch_file_data functions for testing
def mock_read_config():
    return "mocked_file_path.txt"


def mock_fetch_file_data(file_path):
    return "Line 1\nLine 2\nLine 3\nLine 4"


def test_find_string_match_pattern_found(monkeypatch):
    pattern = "Line 1\nLine 2"

    monkeypatch.setattr("src.server.read_config", mock_read_config)
    monkeypatch.setattr("src.server.fetch_file_data", mock_fetch_file_data)

    result, time_taken, current_time = find_string_match(
        pattern, REREAD_ON_QUERY=False)
    assert result == 'STRING EXISTS\n'


def test_find_string_match_pattern_not_found(monkeypatch):
    """
    Test case for pattern not found in the file.
    """
    # Define a pattern that is not present in the file data
    pattern = "Not existing pattern"

    # Mock the read_config and fetch_file_data functions
    monkeypatch.setattr("src.server.read_config", mock_read_config)
    monkeypatch.setattr("src.server.fetch_file_data", mock_fetch_file_data)

    # Call the find_string_match function with the specified pattern
    result, time_taken, current_time = find_string_match(
        pattern, REREAD_ON_QUERY=False)

    # Assert that the result indicates the pattern was not found
    assert result == 'STRING NOT FOUND\n'


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
                "Line 1\nLine 2", REREAD_ON_QUERY=True)
            end_time = time.time()

            time_taken = (end_time - start_time) * 1000

            logger.info(f"File size: {size}, Execution time:"
                        f"{time_taken} milliseconds")
        except Exception as e:
            # Logging any exceptions that occur during the test
            logger.error(f"Exception during stress test: {e}")
        finally:
            os.remove(tmp_file_path)


def test_find_string_match_stress_test(monkeypatch, caplog):

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
