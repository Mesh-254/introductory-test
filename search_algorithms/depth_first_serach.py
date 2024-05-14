def dfs_search(text: str, pattern: str) -> bool:
    """
    Performs Depth-first search to find
      a whole line matching of the pattern in the text.

    Args:
        text (str): The text to search within.
        pattern (str): The pattern to search for.

    Returns:
        bool: True if the whole line matching
        of the pattern is found in the text, False otherwise.
    """
    def dfs_helper(start_index: int, pattern: str) -> bool:
        """
        Helper function for Depth-first search.

        Args:
            start_index (int): The starting index for the search.
            pattern (str): The pattern to search for.

        Returns:
            bool: True if the whole line matching of
            the pattern is found in the text, False otherwise.
        """
        # Base case: If the start index is greater than or
        # equal to the length of the text,
        # return False indicating no match found.
        if start_index >= len(text):
            return False

        # Find the index of the next newline character starting from the
        # current start index.
        newline_index = text.find('\n', start_index)

        # If no newline character is found from the start index onwards,
        # set the end index to the end of the text.
        if newline_index == -1:
            end_index = len(text)
        else:
            # Otherwise, set the end index to the index of the newline
            # character found.
            end_index = newline_index

        # Extract the current line from the text.
        current_line = text[start_index:end_index]

        # If the current line matches the pattern, return True.
        if current_line.strip() == pattern.strip():
            return True

        # Recursively search for the pattern in the remaining text after the
        # current line.
        return dfs_helper(end_index + 1, pattern)

    # Start the Depth-first search from the beginning of the text.
    return dfs_helper(0, pattern)
