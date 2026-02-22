import pytest

from utils import sanitize_filename


class TestSanitizeFilename:
    def test_replaces_spaces_with_underscores(self) -> None:
        assert sanitize_filename("hello world") == "hello_world"

    def test_replaces_invalid_characters(self) -> None:
        assert sanitize_filename('file"name') == "file_name"
        assert sanitize_filename("file:name") == "file_name"
        assert sanitize_filename("file<name>") == "file_name_"
        assert sanitize_filename("file|name") == "file_name"
        assert sanitize_filename("file*name") == "file_name"
        assert sanitize_filename("file?name") == "file_name"

    def test_collapses_multiple_underscores(self) -> None:
        assert sanitize_filename("file   name") == "file_name"
        assert sanitize_filename("file:::name") == "file_name"

    def test_handles_newlines(self) -> None:
        assert sanitize_filename("file\nname") == "file_name"
        assert sanitize_filename("file\r\nname") == "file_name"

    def test_preserves_valid_characters(self) -> None:
        assert sanitize_filename("valid_filename-123.png") == "valid_filename-123.png"

    def test_handles_empty_string(self) -> None:
        assert sanitize_filename("") == ""

    def test_handles_mixed_invalid_characters(self) -> None:
        assert sanitize_filename('a "b" <c> :d:') == "a_b_c_d_"

    @pytest.mark.parametrize(
        ("input_name", "expected"),
        [
            ("Scenario_Then_check_message", "Scenario_Then_check_message"),
            ("My Scenario:Step 1", "My_Scenario_Step_1"),
            ("test<with>brackets", "test_with_brackets"),
        ],
    )
    def test_real_world_scenario_names(self, input_name: str, expected: str) -> None:
        assert sanitize_filename(input_name) == expected
