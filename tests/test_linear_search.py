#!/usr/bin/env python3
import os
import pytest
import logging
import tempfile
import time
from search_algorithms.linear_search import linear_search
from src.server import find_string_match


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_string_exists():
    text = "hello\nworld\nfoo\nbar"
    pattern = "world"
    result = linear_search(text, pattern)
    assert result is True


def test_string_not_found():
    text = "hello\nworld\nfoo\nbar"
    pattern = "baz"
    result = linear_search(text, pattern)
    assert result is False


def test_empty_text():
    text = ""
    pattern = "hello"
    result = linear_search(text, pattern)
    assert result is False


def test_empty_pattern():
    text = "hello\nworld\nfoo\nbar"
    pattern = ""
    result = linear_search(text, pattern)
    assert result is False


def test_pattern_longer_than_text():
    text = "hello"
    pattern = "hello world"
    result = linear_search(text, pattern)
    assert result is False


def test_multiline_text():
    text = "hello world\nhello\nworld\nfoo\nbar"
    pattern = "hello world"
    result = linear_search(text, pattern)
    assert result is True


def test_whitespace_ignored():
    text = "   hello world   \nhello\nworld\nfoo\nbar"
    pattern = "hello world"
    result = linear_search(text, pattern)
    assert result is True


def test_whitespace_in_pattern():
    text = "hello world\nhello\nworld\nfoo\nbar"
    pattern = "   hello world   "
    result = linear_search(text, pattern)
    assert result is True


def test_exact_match():
    text = "   hello world   \nhello\nworld\nfoo\nbar"
    pattern = "   hello world   "
    result = linear_search(text, pattern)
    assert result is True


def test_find_string_match_execution_time(monkeypatch):
    file_sizes = [10000, 50000, 100000, 500000, 1000000]

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

            logger.info(f"File size: {size}, Execution time: {
                        time_taken} milliseconds")
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
                logger.info(f"File size: {file_size}, Queries per second: {query_count},"
                             f"Average execution time per query: {total_time_taken:.4f} milliseconds")

                # Asserting that the result indicates string exists
                assert result[0] == "STRING EXISTS\n"

            except Exception as e:

                # Logging any exceptions that occur during the test
                logger.error(f"Exception during stress test: {e}")

    # Document the limitations of the software
    logger.error(
        "Reached the point where the server can no longer handle the load.")
