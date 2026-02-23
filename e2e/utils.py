"""Shared utilities for E2E test infrastructure."""

from enum import Enum


class ScreenshotMode(Enum):
    """Controls which BDD steps trigger screenshot capture."""

    ALL = "all"
    THEN = "then"
    DISABLED = "false"

    @classmethod
    def from_env(cls, value: str | None) -> ScreenshotMode:
        """Parse an environment variable value into a ScreenshotMode."""
        if value is None:
            return cls.THEN
        try:
            return cls(value.lower())
        except ValueError:
            return cls.THEN

    def should_capture(self, step_keyword: str) -> bool:
        """Determine whether a screenshot should be taken for the given step keyword."""
        if self is ScreenshotMode.ALL:
            return True
        if self is ScreenshotMode.THEN:
            return step_keyword.lower() == "then"
        return False


def sanitize_filename(name: str) -> str:
    """Sanitize filename by removing invalid characters."""
    invalid_chars = '":<>|*?\r\n'
    for char in invalid_chars:
        name = name.replace(char, "_")
    name = name.replace(" ", "_")
    while "__" in name:
        name = name.replace("__", "_")
    return name
