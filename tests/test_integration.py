"""Integration tests for TTS and ASR functionality.

These tests verify that the TTS and ASR services work correctly with real API calls.
Requires proper credentials to be set via environment variables or config files.
"""

import os
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from audiogram_cli.main import audiogram_cli


class TestTTSIntegration:
    """Integration tests for Text-to-Speech functionality."""

    def test_tts_synthesize_russian_gandzhaev_voice(self):
        """Test TTS synthesis with Russian text using gandzhaev voice.
        
        Test scenario: Synthesize phrase "Тестирование синтеза прошло успешно" 
        using gandzhaev voice.
        """
        runner = CliRunner()
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            output_file = tmp_file.name
        
        try:
            # Test command: tts file --voice-name gandzhaev --text "Тестирование синтеза прошло успешно"
            result = runner.invoke(audiogram_cli, [
                "--config", "config.ini",
                "tts", "file",
                "--voice-name", "gandzhaev",
                "--text", "Тестирование синтеза прошло успешно",
                "--output-file", output_file,
                "--sample-rate", "16000"
            ])
            
            # Verify command execution
            if result.exit_code != 0:
                pytest.fail(f"TTS command failed with exit code {result.exit_code}.\n"
                          f"Output: {result.output}\n"
                          f"Exception: {result.exception}")
            
            # Verify output file was created
            assert os.path.exists(output_file), f"Output file {output_file} was not created"
            
            # Verify file has content (audio data)
            file_size = os.path.getsize(output_file)
            assert file_size > 1000, f"Output file too small ({file_size} bytes), likely empty or corrupted"
            
            # Verify expected content in output
            assert "gandzhaev" in result.output, "Voice name not found in output"
            assert "Synthesized audio stored" in result.output or "audio stored" in result.output.lower(), \
                "Success message not found in output"
                
            print(f"✅ TTS Test PASSED: Generated {file_size} bytes of audio")
            print(f"   Voice: gandzhaev")
            print(f"   Text: Тестирование синтеза прошло успешно")
            print(f"   Output: {output_file}")
            
        finally:
            # Clean up temporary file
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_tts_synthesize_english_fallback(self):
        """Test TTS synthesis with English text as a fallback test."""
        runner = CliRunner()
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            output_file = tmp_file.name
        
        try:
            result = runner.invoke(audiogram_cli, [
                "--config", "config.ini",
                "tts", "file",
                "--voice-name", "gandzhaev",
                "--text", "Testing synthesis completed successfully",
                "--output-file", output_file,
                "--sample-rate", "16000"
            ])
            
            if result.exit_code != 0:
                pytest.fail(f"TTS English fallback test failed with exit code {result.exit_code}.\n"
                          f"Output: {result.output}\n"
                          f"Exception: {result.exception}")
            
            assert os.path.exists(output_file), f"Output file {output_file} was not created"
            file_size = os.path.getsize(output_file)
            assert file_size > 1000, f"Output file too small ({file_size} bytes)"
            
            print(f"✅ TTS English Test PASSED: Generated {file_size} bytes of audio")
            
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)


class TestASRIntegration:
    """Integration tests for Automatic Speech Recognition functionality."""

    def test_asr_recognize_1297_wav_with_punctuation(self):
        """Test ASR recognition of 1297.wav file with punctuation enabled.
        
        Test scenario: Recognize 1297.wav with punctuation support.
        """
        runner = CliRunner()
        
        # Verify test audio file exists
        audio_file = "1297.wav"
        assert os.path.exists(audio_file), f"Test audio file {audio_file} not found"
        
        # Test command: asr file --audio-file 1297.wav --model e2e-v3 --enable-punctuator
        result = runner.invoke(audiogram_cli, [
            "--config", "config.ini",
            "asr", "file",
            "--audio-file", audio_file,
            "--model", "e2e-v3",
            "--enable-punctuator"
        ])
        
        # Verify command execution
        if result.exit_code != 0:
            pytest.fail(f"ASR command failed with exit code {result.exit_code}.\n"
                      f"Output: {result.output}\n"
                      f"Exception: {result.exception}")
        
        # Verify expected content in output
        assert "Punctuator enabled: True" in result.output, "Punctuator not enabled in output"
        assert "Hypothesis" in result.output, "No recognition hypothesis found in output"
        assert "is_final: True" in result.output, "No final recognition result found"
        
        # Extract recognized text for verification
        lines = result.output.split('\n')
        hypothesis_lines = [line for line in lines if 'Hypothesis' in line and 'is_final: True' in line]
        
        assert len(hypothesis_lines) > 0, "No final hypothesis found in output"
        
        # Get the recognized text (extract text between quotes)
        recognized_text = ""
        for line in hypothesis_lines:
            if '"' in line:
                start_quote = line.find('"')
                end_quote = line.rfind('"')
                if start_quote != -1 and end_quote != -1 and start_quote < end_quote:
                    recognized_text += line[start_quote+1:end_quote] + " "
        
        recognized_text = recognized_text.strip()
        
        print(f"✅ ASR Test PASSED")
        print(f"   Audio file: {audio_file}")
        print(f"   Model: e2e-v3")
        print(f"   Punctuation: enabled")
        print(f"   Recognized text: '{recognized_text}'")
        
        # Basic validation that we got some text
        assert len(recognized_text) > 0, "No recognized text extracted from output"
        
        return recognized_text

    def test_asr_recognize_without_punctuation(self):
        """Test ASR recognition without punctuation as comparison."""
        runner = CliRunner()
        
        audio_file = "1297.wav"
        assert os.path.exists(audio_file), f"Test audio file {audio_file} not found"
        
        result = runner.invoke(audiogram_cli, [
            "--config", "config.ini",
            "asr", "file", 
            "--audio-file", audio_file,
            "--model", "e2e-v3"
        ])
        
        if result.exit_code != 0:
            pytest.fail(f"ASR without punctuation failed with exit code {result.exit_code}.\n"
                      f"Output: {result.output}\n"
                      f"Exception: {result.exception}")
        
        assert "Punctuator enabled: False" in result.output, "Punctuator should be disabled"
        assert "Hypothesis" in result.output, "No recognition hypothesis found"
        
        print(f"✅ ASR Test (no punctuation) PASSED")


class TestModelService:
    """Test model service functionality."""
    
    def test_get_models_info(self):
        """Test that we can retrieve model information."""
        runner = CliRunner()
        
        result = runner.invoke(audiogram_cli, [
            "--config", "config.ini",
            "models"
        ])
        
        if result.exit_code != 0:
            pytest.fail(f"Models command failed with exit code {result.exit_code}.\n"
                      f"Output: {result.output}\n"
                      f"Exception: {result.exception}")
        
        # Should contain model information
        assert "Model:" in result.output or "model" in result.output.lower(), \
            "No model information found in output"
        
        print(f"✅ Models Test PASSED")
        print("   Retrieved model information successfully")


# Pytest fixtures and configuration
@pytest.fixture(scope="session", autouse=True)
def check_credentials():
    """Check that required credentials are available before running tests."""
    required_env_vars = ["AUDIOGRAM_CLIENT_ID", "AUDIOGRAM_CLIENT_SECRET"]
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        pytest.skip(f"Missing required environment variables: {missing_vars}. "
                   f"Please set them before running integration tests.")


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")


# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration
