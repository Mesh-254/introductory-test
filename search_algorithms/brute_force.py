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
        return False

    # Iterate through each line in the text
    for line in text.splitlines():
        # Check if the current line matches the pattern
        if line == pattern:
            return True  # Match found

    return False  # No match found
