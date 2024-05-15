#!/usr/bin/env python3
from typing import Tuple  # Import Tuple for type hinting


def brute_force_match(pattern: str, text: str) -> bool:
    """
    Performs brute-force string matching to check if pattern matches text line.

    Args:
        pattern (str): The pattern to search for.
        text (str): The text to search in.

    Returns:
        bool: True if pattern matches a line in text, False otherwise.
    """
    m = len(pattern)  # Length of the pattern
    n = len(text)  # Length of the text

    # If the length of the pattern is greater than the length of the text,
    # there can be no match
    if m > n:
        return False  # No match if pattern is longer than text

    # Iterate through each line in the text
    for line in text.splitlines():
        # Check if the current line matches the pattern
        if line == pattern:
            return True  # Match found

    return False  # No match found


file_data = None  # Define a global variable to store file contents


def find_string_match(
        message: str, REREAD_ON_QUERY: bool = True) -> Tuple[str, float, str]:
    """
    Searches for a full match of a string in a file.

    Args:
        message (str): The string to search for.
        REREAD_ON_QUERY (bool): Whether to re-read the file on every query.

    Returns:
        tuple: A tuple containing the search result
        ('STRING EXISTS\n' or 'STRING NOT FOUND\n'),
        time taken to find the match, and the current timestamp.
    """

    global file_data  # Declare file_data as a global variable

    file_path = read_config()  # Getting the file path from configuration

    # Re-read the file on every query or if file_data is not present
    if REREAD_ON_QUERY or file_data is None:
        file_data = fetch_file_data(file_path)  # Fetch the file data

    start_time = time.time()  # Recording the start time of search

    # Split the message into lines to match against the file data
    pattern_lines = message.splitlines()
    text_lines = file_data.splitlines()  # Split the file data into lines

    # Iterate through each line in the file data
    for line in text_lines:
        # Check if the current line matches the message using brute force
        if brute_force_match(line, message):
            end_time = time.time()  # Recording the end time
            time_taken = end_time - start_time  # Calculating the time taken
            current_time = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime())  # Getting the current timestamp
            # Returning match result, time taken, and timestamp
            return 'STRING EXISTS\n', time_taken, current_time

    end_time = time.time()  # Recording the end time
    time_taken = end_time - start_time  # Calculating the time taken
    current_time = time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.localtime())  # Getting the current timestamp
    # Returning match result, time taken, and timestamp
    return 'STRING NOT FOUND\n', time_taken, current_time
