"""Test for functionality of main.py."""
import pytest
from unittest.mock import patch
from ytdlpllm.main import YTDLPLLM


@pytest.fixture
def mock_llm_interface(mocker):
    """Fixture to create and configure a mock LLMInterface object.

    Args:
        mocker (pytest.fixture): The pytest mocker fixture.

    Returns:
        MagicMock: A mocked LLMInterface object with predefined return
            values.
    """
    # Create a mock LLMInterface object
    mock = mocker.patch("ytdlpllm.llm_interface.LLMInterface", autospec=True)
    # Configure the mock to avoid side effects and to specify return values
    mock_instance = mock.return_value
    mock_instance.invoke_model.return_value = '{"explanation": ["Test Explanation"], "command": "yt-dlp -i input.mp4 output.mp4"}'  # noqa: E501
    return mock_instance


def test_ytdlpllm_run_user_confirmation(mock_llm_interface):
    """Test YTDLPLLM run function with user confirming command execution.

    This test simulates user confirmation ('Y') and checks if the correct
    system command is executed as expected when user input is affirmative.

    Args:
        mock_llm_interface (MagicMock): Mocked LLMInterface provided by the
            fixture.
    """
    # Patching 'input' to simulate user inputs and 'subprocess.run' to
    # prevent actual command execution
    with patch("builtins.input", side_effect=["Y"]), patch(
        "subprocess.run"
    ) as mock_run:
        ytdlpllm = YTDLPLLM(llm_interface=mock_llm_interface)
        ytdlpllm.run("Convert video format")

        # Ensure that subprocess.run was called with the expected command
        mock_run.assert_called_with(
            "yt-dlp -i input.mp4 output.mp4", shell=True
        )


def test_ytdlpllm_run_user_abort(mock_llm_interface):
    """Test YTDLPLLM run function with user aborting command execution.

    This test verifies that no system command is executed when the user input
    indicates a decision to abort ('N').

    Args:
        mock_llm_interface (MagicMock): Mocked LLMInterface provided by the
            fixture.
    """
    # Patching 'input' to simulate user input declining to execute the command
    with patch("builtins.input", side_effect=["N"]), patch(
        "subprocess.run"
    ) as mock_run:
        ytdlpllm = YTDLPLLM(llm_interface=mock_llm_interface)
        ytdlpllm.run("Convert video format")

        # Ensure that subprocess.run was not called due to user cancellation
        specific_args = ("yt-dlp -i input.mp4 output.mp4",)
        assert not any(
            args == specific_args for args, _ in mock_run.call_args_list
        ), "subprocess.run was called with specific undesired arguments"


def test_ytdlpllm_initialization(mock_llm_interface):
    """Test the initialization of the YTDLPLLM class.

    Ensures that the YTDLPLLM class is correctly initialized with the provided
    LLMInterface mock.

    Args:
        mock_llm_interface (MagicMock): Mocked LLMInterface provided by the
            fixture.
    """
    ytdlpllm = YTDLPLLM(llm_interface=mock_llm_interface)
    assert ytdlpllm.llm_interface is mock_llm_interface


def test_ytdlpllm_chat(mock_llm_interface):
    """Test the chat function of the YTDLPLLM class.

    Verifies that the chat function returns correct explanations and commands
    based on the mock LLMInterface's behavior.

    Args:
        mock_llm_interface (MagicMock): Mocked LLMInterface provided by the
            fixture.
    """
    ytdlpllm = YTDLPLLM(llm_interface=mock_llm_interface)
    explanation, command = ytdlpllm.chat("Convert video format")
    assert "Test Explanation" in explanation
    assert "yt-dlp -i input.mp4 output.mp4" == command


def test_missing_ytdlp_executable(mock_llm_interface):
    """Test the graceful exit path if yt-dlp is not found.

    Patches the behavior of shutil.which detects the yt-dlp executable
    to return None, which is the behavior if it doesn't find it.

    Args:
        mock_llm_interface (MagicMock): Mocked LLMInterface provided by the
            fixture.
    """
    with pytest.raises(SystemExit) as e, patch(
        "shutil.which", side_effect=[None]
    ):
        _ = YTDLPLLM(mock_llm_interface)
    assert e.type == SystemExit
    assert e.value.code == 1