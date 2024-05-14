import time  # Importing time module for time-related operations


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
        if pattern in line:  # Check if the pattern exists in the current line
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
