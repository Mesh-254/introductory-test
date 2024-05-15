import time

from src.server import fetch_file_data, read_config


def naive_string_match(pattern: str, text: str) -> tuple:
    """
    Performs Naive String Matching to check if
    pattern matches any line in text.

    Args:
        pattern (str): The pattern to search for.
        text (str): The text to search in.

    Returns:
        tuple: A tuple containing the search result,
        time taken to find the match, and the current timestamp.
    """
    start_time = time.time()  # Recording the start time of search

    # Perform Naive String Matching by iterating through each line in the text
    for line in text.splitlines():
        # Check if the pattern matches the current line
        if pattern == line.strip():
            end_time = time.time()  # Recording the end time
            time_taken = end_time - start_time  # Calculating the time taken
            current_time = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime())  # Getting current timestamp
            # Returning match result, time taken, and timestamp
            return 'STRING EXISTS\n', time_taken, current_time

    # If no match is found, record end time, calculate time taken, and get
    # current timestamp
    end_time = time.time()
    time_taken = end_time - start_time
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # Returning match result, time taken, and timestamp
    return 'STRING NOT FOUND\n', time_taken, current_time


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

    # Call naive_string_match function to search for the pattern in the file
    # data
    result, time_taken, current_time = naive_string_match(message, file_data)

    # Returning match result, time taken, and timestamp
    return result, time_taken, current_time
