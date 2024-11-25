import pytest, os
from datetime import datetime

def test_write_read_file(): # a function to test if the system file I/O works as expected 
    # Define the filename and the string to write
    filename = 'test_file.txt'
    content_to_write = "2020-01-12"
    # Write the content to the file
    with open(filename, 'w') as f:
        f.write(content_to_write)
    # Read the content back from the file
    with open(filename, 'r') as f:
        content_read = f.read().strip()  # Use .strip() to remove any extra whitespace/newlines
    # Assert that the content read matches the content written
    assert content_read == content_to_write
    # Clean up the test file after the test
    os.remove(filename)
    