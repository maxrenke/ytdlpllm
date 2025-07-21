"""Test for functionality of openai_llm.py."""
import pytest
from ytdlpllm.openai_llm import OpenAILLMInterface


def test_missing_openai_api_key(monkeypatch):
    """Test that missing OPENAI_API_KEY does not cause exit when using Ollama.

    Args:
        monkeypatch (_pytest.monkeypatch.MonkeyPatch): A pytest fixture
    """
    # Temporarily unset OPENAI_API_KEY
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    # Should not raise SystemExit when using Ollama
    try:
        llm = OpenAILLMInterface(
            "llama3:latest",
            base_url="http://localhost:11434/v1",
            api_key="dummy-key",
        )
    except SystemExit:
        pytest.fail("SystemExit was raised, but missing OPENAI_API_KEY should be allowed for Ollama.")
