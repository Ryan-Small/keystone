"""Shared utilities for E2E test infrastructure."""


def sanitize_filename(name: str) -> str:
    """Sanitize filename by removing invalid characters."""
    invalid_chars = '":<>|*?\r\n'
    for char in invalid_chars:
        name = name.replace(char, "_")
    name = name.replace(" ", "_")
    while "__" in name:
        name = name.replace("__", "_")
    return name
