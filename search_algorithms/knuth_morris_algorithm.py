from typing import Tuple, List
import time
from src.server import read_config, fetch_file_data


def knuth_search(text: str, pattern: str) -> bool:
    """
    Performs Knuth–Morris–Pratt search to find
    a whole line matching of the pattern in the text.

    Args:
        text (str): The text to search within.
        pattern (str): The pattern to search for.

    Returns:
        bool: True if the whole line matching
        of the pattern is found in the text, False otherwise.
    """
    def compute_prefix_function(pattern: str) -> List[int]:
        """
        Computes the prefix function for the pattern.

        Args:
            pattern (str): The pattern string.

        Returns:
            list: The prefix function for the pattern.
        """
        m = len(pattern)
        pi = [0] * m
        k = 0
        for q in range(1, m):
            while k > 0 and pattern[k] != pattern[q]:
                k = pi[k - 1]
            if pattern[k] == pattern[q]:
                k += 1
            pi[q] = k
        return pi

    n = len(text)
    m = len(pattern)
    pi = compute_prefix_function(pattern)
    q = 0
    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q - 1]
        if pattern[q] == text[i]:
            q += 1
        if q == m:
            # Ensure that the entire line matches the pattern
            line_start = i - m + 1
            line_end = i
            while line_start >= 0 and text[line_start] != '\n':
                line_start -= 1
            while line_end < n and text[line_end] != '\n':
                line_end += 1
            line = text[line_start + 1:line_end]
            if line == pattern:
                return True
            # Reset q for next iteration
            q = 0
    return False


file_data = None


def find_string_match(
        message: str, REREAD_ON_QUERY: bool = False) -> Tuple[str, float, str]:
    """
    Searches for a full match of a string
    in a file using Knuth–Morris–Pratt search.

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

    # Split the text into lines
    text_lines = file_data.splitlines()

    # Search for the pattern in each line
    # of the text using Knuth–Morris–Pratt search
    for line in text_lines:
        if knuth_search(line, message):
            end_time = time.time()  # Recording the end time
            time_taken = end_time - start_time  # Calculating the time taken
            current_time = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime())  # Getting current timestamp
            # Returning match result, time taken, and timestamp
            return 'STRING EXISTS\n', time_taken, current_time

    end_time = time.time()  # Recording the end time
    time_taken = end_time - start_time  # Calculating the time taken
    current_time = time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.localtime())  # Getting current timestamp
    # Returning match result, time taken, and timestamp
    return 'STRING NOT FOUND\n', time_taken, current_time
