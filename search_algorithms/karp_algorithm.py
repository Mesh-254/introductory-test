import time
import sys


def karp_rabin_string_match(pattern: str, text: str) -> tuple:
    """
    Performs Karp-Rabin String Matching to check
      if pattern matches any line in text.

    Args:
        pattern (str): The pattern to search for.
        text (str): The text to search in.

    Returns:
        tuple: A tuple containing the search result,
        time taken to find the match, and the current timestamp.
    """
    prime = 101  # A prime number to reduce hash collisions
    pattern_length = len(pattern)  # Length of the pattern
    text_length = len(text)  # Length of the text
    pattern_hash = hash(pattern)  # Hash value of the pattern
    start_time = time.time()  # Recording the start time of search

    # Calculate hash of pattern and first window of text
    text_hash = hash(text[:pattern_length])

    # Iterate through the text
    for i in range(text_length - pattern_length + 1):
        if pattern_hash == text_hash:
            # Check if the substrings match
            if pattern == text[i:i + pattern_length]:
                end_time = time.time()  # Recording the end time

                # Calculating the time taken
                time_taken = end_time - start_time
                current_time = time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime())  # Getting current timestamp
                # Returning match result, time taken, and timestamp
                return 'STRING EXISTS\n', time_taken, current_time

        # Calculate hash for the next window of text
        if i < text_length - pattern_length:
            text_hash = (prime * (text_hash - ord(text[i]) * (prime ** (
                pattern_length - 1))) +
                ord(text[i + pattern_length])) % sys.maxsize

    # If no match is found, record end time, calculate time taken, and get
    # current timestamp
    end_time = time.time()
    time_taken = end_time - start_time
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # Returning match result, time taken, and timestamp
    return 'STRING NOT FOUND\n', time_taken, current_time


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

    # Call karp_rabin_string_match function to search for the pattern in the
    # file data
    result, time_taken, current_time = karp_rabin_string_match(
        message, file_data)

    end_time = time.time()  # Recording the end time

    # Calculating the time taken
    time_taken = end_time - start_time

    # Returning match result, time taken, and timestamp
    return result, time_taken, current_time
