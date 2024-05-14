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
    skip_table = preprocess(
        pattern)  # Preprocess the pattern to generate the skip table
    n = len(text)  # Get the length of the text
    m = len(pattern)  # Get the length of the pattern
    i = m - 1  # Set the index in pattern to the last character
    j = m - 1  # Set the index in text to the last character

    # Iterate over the text
    while j < n:
        # Check if the current characters in pattern and text match
        if text[j] == pattern[i]:
            # If the characters match and
            # we've reached the start of the pattern,
            # a match is found, so return True
            if i == 0:
                return True
            else:
                # Move to the previous characters in pattern and text
                i -= 1
                j -= 1
        else:
            # If the characters don't match, adjust the index in text based on
            # the skip table
            if j + 1 >= n:
                break
            else:
                j += m - min(i, 1 + skip_table.get(text[j], -1))
                i = m - 1

    return False  # No match found
