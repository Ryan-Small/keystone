import pytest

from utils import ScreenshotMode, sanitize_filename


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


class TestScreenshotMode:
    def test_enum_values(self) -> None:
        assert ScreenshotMode.ALL.value == "all"
        assert ScreenshotMode.THEN.value == "then"
        assert ScreenshotMode.DISABLED.value == "false"

    def test_from_env_defaults_to_then(self) -> None:
        assert ScreenshotMode.from_env(None) is ScreenshotMode.THEN

    def test_from_env_case_insensitive(self) -> None:
        assert ScreenshotMode.from_env("ALL") is ScreenshotMode.ALL
        assert ScreenshotMode.from_env("Then") is ScreenshotMode.THEN
        assert ScreenshotMode.from_env("FALSE") is ScreenshotMode.DISABLED

    def test_from_env_invalid_defaults_to_then(self) -> None:
        assert ScreenshotMode.from_env("invalid") is ScreenshotMode.THEN

    def test_should_capture_all_mode(self) -> None:
        assert ScreenshotMode.ALL.should_capture("given") is True
        assert ScreenshotMode.ALL.should_capture("then") is True
        assert ScreenshotMode.ALL.should_capture("when") is True

    def test_should_capture_then_mode(self) -> None:
        assert ScreenshotMode.THEN.should_capture("then") is True
        assert ScreenshotMode.THEN.should_capture("given") is False
        assert ScreenshotMode.THEN.should_capture("when") is False

    def test_should_capture_disabled_mode(self) -> None:
        assert ScreenshotMode.DISABLED.should_capture("then") is False
        assert ScreenshotMode.DISABLED.should_capture("given") is False
