import time
from typing import Tuple
# Import custom functions from the server module
from src.server import fetch_file_data, read_config


def boyer_moore(pattern_lines, text_lines):
    """
    Boyer-Moore algorithm modified to search for complete lines in the text.

    Args:
        pattern_lines (List[str]): The lines of the pattern to search for.
        text_lines (List[str]): The lines of the
        text containing lines to search.

    Returns:
        int: The index of the first occurrence of
        the pattern in the text, or -1 if not found.
    """
    pattern_length = len(pattern_lines)  # Get the length of the pattern
    text_length = len(text_lines)  # Get the length of the text

    # Preprocess the pattern for faster searching by creating the skip table
    skip = {pattern_lines[i]: pattern_length -
            i - 1 for i in range(pattern_length - 1)}
    skip[''] = pattern_length  # If pattern is empty, skip the entire pattern

    index = pattern_length - 1  # Start searching from the end of the pattern

    while index < text_length:
        # Get the current lines to match against the pattern
        lines_to_match = text_lines[index:index + pattern_length]

        # Check if the lines to match match the pattern
        if lines_to_match == pattern_lines:
            return index  # Return the start index of the matched lines

        # Update index to jump to the next possible occurrence of pattern
        if lines_to_match[-1] in skip:
            index += skip[lines_to_match[-1]]
        else:
            index += pattern_length

    return -1  # Pattern not found


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
        tuple: A tuple containing the search result
        ('STRING EXISTS\n' or 'STRING NOT FOUND\n'),
        time taken to find the match, and the current timestamp.
    """

    global file_data  # Declare file_data as a global variable

    file_path = read_config()  # Get the file path from configuration

    # Re-read the file on every query or if file_data is not present
    if REREAD_ON_QUERY or file_data is None:
        file_data = fetch_file_data(file_path)

    start_time = time.time()  # Record the start time of the search

    # Split the message into lines to match against the file data
    pattern_lines = message.splitlines()
    text_lines = file_data.splitlines()  # Split the file data into lines

    # Search for the pattern in the text using Boyer-Moore algorithm
    index = boyer_moore(pattern_lines, text_lines)

    if index != -1:
        end_time = time.time()  # Record the end time
        time_taken = end_time - start_time  # Calculate the time taken
        current_time = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime())  # Get the current timestamp
        # Return match result, time taken, and timestamp
        return 'STRING EXISTS\n', time_taken, current_time

    end_time = time.time()  # Record the end time
    time_taken = end_time - start_time  # Calculate the time taken
    current_time = time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.localtime())  # Get the current timestamp
    # Return match result, time taken, and timestamp
    return 'STRING NOT FOUND\n', time_taken, current_time
