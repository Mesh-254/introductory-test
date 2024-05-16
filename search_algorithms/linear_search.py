#!/usr/bin/env python3
import time
from src.server import fetch_file_data, read_config


def linear_search(text: str, pattern: str) -> bool:
    """
    Performs linear search to find a whole
    line matching of the pattern in the text.

    Args:
        text (str): The text to search within.
        pattern (str): The pattern to search for.

    Returns:
        bool: True if the whole line matching of
        the pattern is found in the text, False otherwise.
    """
    # Split the text into lines
    lines = text.split('\n')

    # Iterate through each line in the text
    for line in lines:
        # Check if the current line matches the pattern (ignoring leading and
        # trailing whitespaces)
        if line.strip() == pattern.strip():
            return True  # Whole line matching found

    return False  # Whole line matching not found


# Define a global variable to store file contents
file_data = None


def find_string_match(
        message: str, REREAD_ON_QUERY: bool = False) -> tuple:
    """
    Searches for a full match of a string in a file.

    Args:
        message (str): The string to search for.
        REREAD_ON_QUERY (bool): Whether to re-read the file on every query.

    Returns:
        tuple: A tuple containing the search result,
        time taken to find the match, and the current timestamp.
    """

    # Declare file_data as a global variable
    global file_data

    file_path = read_config()  # Getting the file path from configuration

    # Re-read the file on every query or if file_data is not present
    if REREAD_ON_QUERY or file_data is None:
        file_data = fetch_file_data(file_path)

    start_time = time.time()  # Recording the start time of search

    # Call linear_search function to search for the pattern in the file data
    result = linear_search(file_data, message)

    end_time = time.time()  # Recording the end time

    # Calculating the time taken
    time_taken = end_time - start_time

    # Returning match result, time taken, and timestamp
    if result:
        return 'STRING EXISTS\n', time_taken, time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime())
    else:
        return 'STRING NOT FOUND\n', time_taken, time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime())
