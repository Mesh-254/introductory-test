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
