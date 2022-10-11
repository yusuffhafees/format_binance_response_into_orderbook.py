import base64
def file2str(file: bytes):
    """
    Converts a bytes-like object to a file by first enconding it in base64. To be used for safe file transfer via
    string-only mediums.
    Args:
        file: A bytes-representation of the file
    Returns:
        A base64 encoded string representation of the file
    """
    return base64.b64encode(file).decode()

def str2file(string: str):
    """
        Converts a string object to a file by first decoding it in base64. To be used for backwards conversion of a file
        sent through string-only mediums.
        Args:
            string: A string-representation of the file in base64
        Returns:
            A bytes representation of the file
        """
    return base64.b64decode(string.encode())