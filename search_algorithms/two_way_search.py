#!/usr/bin/env python3
from typing import Tuple


def preprocess(pattern: str) -> dict:
    """
    Preprocesses the pattern to generate a skip table.

    Args:
        pattern (str): The pattern to preprocess.

    Returns:
        dict: A dictionary containing the skip table
        for characters in the pattern.
    """
    skip_table = {}  # Create an empty dictionary for the skip table
    m = len(pattern)  # Get the length of the pattern

    # Iterate over the characters in the pattern
    for i in range(m):
        # Calculate the skip value for the current character and add it to the
        # skip table
        skip_table[pattern[i]] = m - i - 1

    return skip_table  # Return the skip table


def two_way_string_match(pattern: str, text: str) -> bool:
    """
    Performs Two-Way String Matching to find a match of a line in the text.

    Args:
        pattern (str): The pattern to search for.
        text (str): The text to search within.

    Returns:
        bool: True if a match of a line is found in the text, False otherwise.
    """
    # Preprocess the pattern to generate the skip table
    skip_table = preprocess(pattern)
    pattern_lines = pattern.splitlines()  # Split the pattern into lines
    text_lines = text.splitlines()  # Split the text into lines
    m = len(pattern_lines)  # Get the number of lines in the pattern
    n = len(text_lines)  # Get the number of lines in the text

    # Iterate over the text
    for i in range(n - m + 1):
        # Check if the lines in the text match the lines in the pattern
        if text_lines[i:i + m] == pattern_lines:
            return True  # Match found

    return False  # No match found


# Define a global variable to store file contents
file_data = None


def find_string_match(
        message: str, REREAD_ON_QUERY: bool = True) -> Tuple[str, float, str]:
    """
    Searches for a full match of a string in a file.

    Args:
        message (str): The string to search for.
        REREAD_ON_QUERY (bool): Whether to re-read the file on every query.

    Returns:
        tuple: A tuple containing the search result,
        time taken to find the match,
               and the current timestamp.
    """

    # Declare file_data as a global variable
    global file_data

    file_path = read_config()  # Getting the file path from configuration

    # Re-read the file on every query or if file_data is not present
    if REREAD_ON_QUERY or file_data is None:
        file_data = fetch_file_data(file_path)

    start_time = time.time()  # Recording the start time of search

    # Check if the message exists as a full line in the file data
    if two_way_string_match(message, file_data.strip()):
        end_time = time.time()  # Recording the end time
        time_taken = end_time - start_time  # Calculating the time taken
        current_time = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime())  # Getting current timestamp
        # Returning match result, time taken, and timestamp
        return 'STRING EXISTS\n', time_taken, current_time
    else:
        end_time = time.time()  # Recording the end time
        time_taken = end_time - start_time  # Calculating the time taken
        current_time = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime())  # Getting current timestamp
        # Returning match result, time taken, and timestamp
        return 'STRING NOT FOUND\n', time_taken, current_time
