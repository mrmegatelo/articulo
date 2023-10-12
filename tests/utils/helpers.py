"""
Helpers for tests
"""

import os


def read_html_text(file_name: str):
    """
    Returns html fixture file content by name
    """
    file_path = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "fixtures_html", file_name)
    )
    with open(file_path, "r", encoding="utf8") as file:
        content = file.read()
        return content


def read_html_bytes(file_name: str, encoding="utf8"):
    """
    Returns html fixture file content by name
    """
    text = read_html_text(file_name)
    return text.encode(encoding)
