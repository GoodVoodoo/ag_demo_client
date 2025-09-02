"""
Integration tests for TTS and ASR functionality.

These tests verify that the Audiogram services are working correctly with real API calls.
Tests require valid credentials to be configured.

Test scenarios:
1. Russian TTS - synthesize phrase "Тестирование синтеза прошло успешно" using gandzhaev voice
2. English TTS - synthesize English phrase using voice 2 with eng voice model
3. ASR - recognize 1297.wav with punctuation enabled
"""

import os
import tempfile
from pathlib import Path

import pytest

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # python-dotenv not available, continue without it
    pass

from audiogram_client.common_utils.config import Settings
from audiogram_client.common_utils.types import ASAttackType, TTSVoiceStyle, VADAlgo, VADMode, VAResponseMode


class TestIntegration:
    """Integration tests for TTS and ASR services."""

    @pytest.fixture(scope="class")
    def settings(self):
        """Create settings instance for tests."""
        config_path = Path(__file__).parent.parent / "config.ini"
        settings = Settings([str(config_path)])
        
        # Validate that credentials are available
        try:
            settings.validators.validate()
        except Exception as e:
            pytest.skip(f"Configuration validation failed: {e}")
        
        return settings

    @pytest.fixture(scope="class")
    def test_audio_file(self):
        """Path to the test audio file for ASR."""
        audio_path = Path(__file__).parent.parent / "1297.wav"
        if not audio_path.exists():
            pytest.skip(f"Test audio file not found: {audio_path}")
        return str(audio_path)

    def test_tts_gandzhaev_voice(self, settings):
        """
        Test TTS synthesis with gandzhaev voice.
        
        Synthesizes the phrase "Тестирование синтеза прошло успешно" 
        and verifies that audio is generated successfully.
        """
        from audiogram_client.tts.utils.request import make_tts_request
        from audiogram_client.common_utils.auth import get_auth_metadata
        from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
        from audiogram_client.genproto import tts_pb2, tts_pb2_grpc
        
        test_text = "Тестирование синтеза прошло успешно"
        voice_name = "gandzhaev"
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            output_file = temp_file.name
        
        try:
            # Get auth metadata
            auth_metadata = get_auth_metadata(
                settings.sso_url,
                settings.realm,
                settings.client_id,
                settings.client_secret,
                settings.iam_account,
                settings.iam_workspace,
                settings.verify_sso,
            )

            # Create TTS request
            request = make_tts_request(
                text=test_text,
                is_ssml=False,
                voice_name=voice_name,
                rate=22050,  # gandzhaev voice supports 22050 Hz
                model_type=None,  # Auto-detect
                model_rate=None,  # Auto-detect
                voice_style=TTSVoiceStyle.neutral,
            )

            # Make gRPC call
            with open_grpc_channel(
                settings.api_address,
                ssl_creds_from_settings(settings),
            ) as channel:
                stub = tts_pb2_grpc.TTSStub(channel)

                response: tts_pb2.SynthesizeSpeechResponse
                response, call = stub.Synthesize.with_call(
                    request,
                    metadata=auth_metadata,
                    timeout=settings.timeout,
                )

            # Save audio to file
            Path(output_file).write_bytes(response.audio)
            
            # Verify that audio file was created and has content
            assert os.path.exists(output_file), "TTS output file was not created"
            
            file_size = os.path.getsize(output_file)
            assert file_size > 1000, f"TTS output file too small: {file_size} bytes"
            
            print(f"✅ TTS test passed: Generated {file_size} bytes of audio for text '{test_text}' with voice '{voice_name}'")
            
        finally:
            # Clean up temporary file
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_tts_english_voice(self, settings):
        """
        Test English TTS synthesis with voice 2.
        
        Synthesizes an English phrase using voice 2 with the eng voice model
        and verifies that audio is generated successfully.
        """
        from audiogram_client.tts.utils.request import make_tts_request
        from audiogram_client.common_utils.auth import get_auth_metadata
        from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
        from audiogram_client.genproto import tts_pb2, tts_pb2_grpc
        
        test_text = "Hello, this is an English text-to-speech integration test."
        voice_name = "voice 2"
        model_type = "eng voice"
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            output_file = temp_file.name
        
        try:
            # Get auth metadata
            auth_metadata = get_auth_metadata(
                settings.sso_url,
                settings.realm,
                settings.client_id,
                settings.client_secret,
                settings.iam_account,
                settings.iam_workspace,
                settings.verify_sso,
            )

            # Create TTS request
            request = make_tts_request(
                text=test_text,
                is_ssml=False,
                voice_name=voice_name,
                rate=22050,  # English voices support 22050 Hz
                model_type=model_type,
                model_rate=None,  # Auto-detect
                voice_style=TTSVoiceStyle.neutral,
                language_code=None,  # Use default (ru) as per model configuration
            )

            # Make gRPC call
            with open_grpc_channel(
                settings.api_address,
                ssl_creds_from_settings(settings),
            ) as channel:
                stub = tts_pb2_grpc.TTSStub(channel)

                response: tts_pb2.SynthesizeSpeechResponse
                response, call = stub.Synthesize.with_call(
                    request,
                    metadata=auth_metadata,
                    timeout=settings.timeout,
                )

            # Save audio to file
            Path(output_file).write_bytes(response.audio)
            
            # Verify that audio file was created and has content
            assert os.path.exists(output_file), "English TTS output file was not created"
            
            file_size = os.path.getsize(output_file)
            assert file_size > 1000, f"English TTS output file too small: {file_size} bytes"
            
            print(f"✅ English TTS test passed: Generated {file_size} bytes of audio for text '{test_text}' with voice '{voice_name}' (model: {model_type})")
            
        finally:
            # Clean up temporary file
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_tts_multiple_english_voices(self, settings):
        """
        Test multiple English voices to ensure variety works.
        
        Tests voice 1 and voice 3 in addition to voice 2 to verify
        that different English voices are accessible and working.
        """
        from audiogram_client.tts.utils.request import make_tts_request
        from audiogram_client.common_utils.auth import get_auth_metadata
        from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
        from audiogram_client.genproto import tts_pb2, tts_pb2_grpc
        
        test_voices = [
            ("voice 1", "Testing English voice one with natural pronunciation."),
            ("voice 3", "Testing English voice three for variety and quality."),
        ]
        
        # Get auth metadata once
        auth_metadata = get_auth_metadata(
            settings.sso_url,
            settings.realm,
            settings.client_id,
            settings.client_secret,
            settings.iam_account,
            settings.iam_workspace,
            settings.verify_sso,
        )
        
        successful_voices = []
        
        for voice_name, test_text in test_voices:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                output_file = temp_file.name
            
            try:
                # Create TTS request
                request = make_tts_request(
                    text=test_text,
                    is_ssml=False,
                    voice_name=voice_name,
                    rate=22050,  # English voices support 22050 Hz
                    model_type="eng voice",
                    model_rate=None,  # Auto-detect
                    voice_style=TTSVoiceStyle.neutral,
                    language_code=None,  # Use default (ru) as per model configuration
                )

                # Make gRPC call
                with open_grpc_channel(
                    settings.api_address,
                    ssl_creds_from_settings(settings),
                ) as channel:
                    stub = tts_pb2_grpc.TTSStub(channel)

                    response: tts_pb2.SynthesizeSpeechResponse
                    response, call = stub.Synthesize.with_call(
                        request,
                        metadata=auth_metadata,
                        timeout=settings.timeout,
                    )

                # Save audio to file
                Path(output_file).write_bytes(response.audio)
                
                # Verify that audio file was created and has content
                assert os.path.exists(output_file), f"English TTS output file was not created for {voice_name}"
                
                file_size = os.path.getsize(output_file)
                assert file_size > 1000, f"English TTS output file too small for {voice_name}: {file_size} bytes"
                
                successful_voices.append((voice_name, file_size))
                
            finally:
                # Clean up temporary file
                if os.path.exists(output_file):
                    os.unlink(output_file)
        
        # Verify that we successfully tested at least one additional voice
        assert len(successful_voices) >= 1, f"Failed to test any additional English voices"
        
        print(f"✅ Multiple English voices test passed: Successfully tested {len(successful_voices)} voices:")
        for voice_name, file_size in successful_voices:
            print(f"   - {voice_name}: {file_size} bytes")

    def test_asr_with_punctuation(self, settings, test_audio_file):
        """
        Test ASR recognition with punctuation enabled.
        
        Recognizes the audio file 1297.wav with punctuation enabled
        and verifies that text is recognized successfully.
        """
        from audiogram_client.common_utils.audio import AudioFile
        from audiogram_client.common_utils.auth import get_auth_metadata
        from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
        from audiogram_client.genproto import stt_pb2, stt_pb2_grpc
        from audiogram_client.asr.utils.request import (
            make_va_config,
            make_antispoofing_config,
            make_speaker_labeling_config,
            make_context_dictionary_config,
            make_recognition_config,
        )
        
        try:
            # Get auth metadata
            auth_metadata = get_auth_metadata(
                settings.sso_url,
                settings.realm,
                settings.client_id,
                settings.client_secret,
                settings.iam_account,
                settings.iam_workspace,
                settings.verify_sso,
            )

            # Load audio file
            audio = AudioFile(test_audio_file)

            # Create configs
            va_config = make_va_config(
                VADAlgo.vad,
                VADMode.default,  # Use default instead of normal
                0.5,
                300,
                300,
                250,
                0.99,
                200,
                300,
                0.5,
                300,
                0.5,
                300,
                0.5,
                300,
                0.5,
            )
            as_config = make_antispoofing_config(
                False,
                None,
                None,
                None,
                None,
            )
            sl_config = make_speaker_labeling_config(
                False,
                None,
                None,
            )
            wfst_config = make_context_dictionary_config(
                "",
                0.0,  # Set weight to 0 when dictionary name is empty
            )
            recognition_config = make_recognition_config(
                "e2e-v3",
                va_config,
                VAResponseMode.disable,
                audio.sample_rate,
                audio.channel_count,
                False,  # enable_genderage
                False,  # enable_word_time_offsets
                True,   # enable_punctuator
                False,  # enable_denormalization
                as_config,
                sl_config,
                wfst_config,
                False,  # split_by_channel
            )

            # Create the request
            request = stt_pb2.FileRecognizeRequest(
                config=recognition_config,
                audio=audio.blob,
            )

            # Make gRPC call
            with open_grpc_channel(
                settings.api_address,
                ssl_creds_from_settings(settings),
            ) as channel:
                stub = stt_pb2_grpc.STTStub(channel)

                response: stt_pb2.FileRecognizeResponse
                response, call = stub.FileRecognize.with_call(
                    request,
                    metadata=auth_metadata,
                    timeout=settings.timeout,
                )

            # Verify that recognition completed successfully
            assert response.response, "No recognition results returned"
            
            # Check that we got some transcribed text
            has_transcription = False
            for result in response.response:
                if result.hypothesis and result.hypothesis.transcript.strip():
                    has_transcription = True
                    break
            
            assert has_transcription, "No transcribed text found in ASR response"
            
            print(f"✅ ASR test passed: Successfully recognized audio file '{test_audio_file}' with punctuation enabled")
            print(f"Found {len(response.response)} result(s)")
            
        except Exception as e:
            pytest.fail(f"ASR recognition failed: {e}")

    def test_credentials_available(self, settings):
        """
        Test that required credentials are available.
        
        This is a prerequisite test to ensure other tests can run.
        """
        assert settings.client_id, "AUDIOGRAM_CLIENT_ID is not configured"
        assert settings.client_secret, "AUDIOGRAM_CLIENT_SECRET is not configured"
        assert settings.api_address, "API address is not configured"
        
        print("✅ Credentials test passed: All required configuration is available")

    def test_audio_file_exists(self, test_audio_file):
        """
        Test that the required audio file exists.
        
        This is a prerequisite test for ASR functionality.
        """
        assert os.path.exists(test_audio_file), f"Test audio file not found: {test_audio_file}"
        
        file_size = os.path.getsize(test_audio_file)
        assert file_size > 1000, f"Test audio file too small: {file_size} bytes"
        
        print(f"✅ Audio file test passed: File '{test_audio_file}' exists ({file_size} bytes)")


class TestAudioKitDevSFIntegration:
    """Integration tests specifically for AudioKit Dev SF endpoint."""

    @pytest.fixture(scope="class")
    def dev_sf_settings(self):
        """Create settings instance for AudioKit Dev SF tests."""
        config_path = Path(__file__).parent.parent / "config_audiokit_dev_sf.ini"
        if not config_path.exists():
            pytest.skip(f"AudioKit Dev SF config file not found: {config_path}")
        
        settings = Settings([str(config_path)])
        
        # Validate that credentials are available
        try:
            settings.validators.validate()
        except Exception as e:
            pytest.skip(f"AudioKit Dev SF configuration validation failed: {e}")
        
        return settings

    def test_dev_sf_credentials_available(self, dev_sf_settings):
        """
        Test that AudioKit Dev SF credentials are available.
        
        This is a prerequisite test to ensure other tests can run.
        """
        assert dev_sf_settings.client_id, "AUDIOGRAM_CLIENT_ID is not configured for AudioKit Dev SF"
        assert dev_sf_settings.client_secret, "AUDIOGRAM_CLIENT_SECRET is not configured for AudioKit Dev SF"
        assert dev_sf_settings.api_address, "API address is not configured for AudioKit Dev SF"
        assert dev_sf_settings.api_address == "asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443", "Incorrect AudioKit Dev SF endpoint"
        
        print("✅ AudioKit Dev SF credentials test passed: All required configuration is available")

    def test_dev_sf_certificate_setup(self, dev_sf_settings):
        """
        Test that the required certificate file exists for AudioKit Dev SF.
        """
        cert_path = Path(__file__).parent.parent / "WinCAG2ANDclass2root.pem"
        if not cert_path.exists():
            pytest.skip(f"Certificate file not found: {cert_path}. Please follow CERTIFICATE_SETUP_DEV_SF.md instructions")
        
        # Check that it's not just a placeholder
        cert_content = cert_path.read_text()
        if "placeholder" in cert_content.lower() or cert_content.startswith("#"):
            pytest.skip("Certificate file appears to be a placeholder. Please replace with actual certificate content")
        
        print(f"✅ AudioKit Dev SF certificate test passed: Certificate file exists at {cert_path}")

    def test_dev_sf_tts_gandzhaev_voice(self, dev_sf_settings):
        """
        Test TTS synthesis with gandzhaev voice on AudioKit Dev SF endpoint.
        
        Synthesizes the phrase "Тестирование AudioKit Dev SF прошло успешно" 
        and verifies that audio is generated successfully.
        """
        from audiogram_client.tts.utils.request import make_tts_request
        from audiogram_client.common_utils.auth import get_auth_metadata
        from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
        from audiogram_client.genproto import tts_pb2, tts_pb2_grpc
        
        test_text = "Тестирование AudioKit Dev SF прошло успешно"
        voice_name = "gandzhaev"
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            output_file = temp_file.name
        
        try:
            # Get auth metadata
            auth_metadata = get_auth_metadata(
                dev_sf_settings.sso_url,
                dev_sf_settings.realm,
                dev_sf_settings.client_id,
                dev_sf_settings.client_secret,
                dev_sf_settings.iam_account,
                dev_sf_settings.iam_workspace,
                dev_sf_settings.verify_sso,
            )

            # Create TTS request
            request = make_tts_request(
                text=test_text,
                is_ssml=False,
                voice_name=voice_name,
                rate=22050,  # gandzhaev voice supports 22050 Hz
                model_type=None,  # Auto-detect
                model_rate=None,  # Auto-detect
                voice_style=TTSVoiceStyle.neutral,
            )

            # Make gRPC call
            with open_grpc_channel(
                dev_sf_settings.api_address,
                ssl_creds_from_settings(dev_sf_settings),
            ) as channel:
                stub = tts_pb2_grpc.TTSStub(channel)

                response: tts_pb2.SynthesizeSpeechResponse
                response, call = stub.Synthesize.with_call(
                    request,
                    metadata=auth_metadata,
                    timeout=dev_sf_settings.timeout,
                )

            # Save audio to file
            Path(output_file).write_bytes(response.audio)
            
            # Verify that audio file was created and has content
            assert os.path.exists(output_file), "AudioKit Dev SF TTS output file was not created"
            
            file_size = os.path.getsize(output_file)
            assert file_size > 1000, f"AudioKit Dev SF TTS output file too small: {file_size} bytes"
            
            print(f"✅ AudioKit Dev SF TTS test passed: Generated {file_size} bytes of audio for text '{test_text}' with voice '{voice_name}'")
            print(f"   Endpoint: {dev_sf_settings.api_address}")
            
        finally:
            # Clean up temporary file
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_dev_sf_tts_english_voice(self, dev_sf_settings):
        """
        Test English TTS synthesis on AudioKit Dev SF endpoint.
        
        Synthesizes an English phrase using voice 2 with the eng voice model
        and verifies that audio is generated successfully.
        """
        from audiogram_client.tts.utils.request import make_tts_request
        from audiogram_client.common_utils.auth import get_auth_metadata
        from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
        from audiogram_client.genproto import tts_pb2, tts_pb2_grpc
        
        test_text = "Hello, this is an AudioKit Dev SF English text-to-speech integration test."
        voice_name = "voice 2"
        model_type = "eng voice"
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            output_file = temp_file.name
        
        try:
            # Get auth metadata
            auth_metadata = get_auth_metadata(
                dev_sf_settings.sso_url,
                dev_sf_settings.realm,
                dev_sf_settings.client_id,
                dev_sf_settings.client_secret,
                dev_sf_settings.iam_account,
                dev_sf_settings.iam_workspace,
                dev_sf_settings.verify_sso,
            )

            # Create TTS request
            request = make_tts_request(
                text=test_text,
                is_ssml=False,
                voice_name=voice_name,
                rate=22050,  # English voices support 22050 Hz
                model_type=model_type,
                model_rate=None,  # Auto-detect
                voice_style=TTSVoiceStyle.neutral,
                language_code=None,  # Use default (ru) as per model configuration
            )

            # Make gRPC call
            with open_grpc_channel(
                dev_sf_settings.api_address,
                ssl_creds_from_settings(dev_sf_settings),
            ) as channel:
                stub = tts_pb2_grpc.TTSStub(channel)

                response: tts_pb2.SynthesizeSpeechResponse
                response, call = stub.Synthesize.with_call(
                    request,
                    metadata=auth_metadata,
                    timeout=dev_sf_settings.timeout,
                )

            # Save audio to file
            Path(output_file).write_bytes(response.audio)
            
            # Verify that audio file was created and has content
            assert os.path.exists(output_file), "AudioKit Dev SF English TTS output file was not created"
            
            file_size = os.path.getsize(output_file)
            assert file_size > 1000, f"AudioKit Dev SF English TTS output file too small: {file_size} bytes"
            
            print(f"✅ AudioKit Dev SF English TTS test passed: Generated {file_size} bytes of audio for text '{test_text}' with voice '{voice_name}' (model: {model_type})")
            print(f"   Endpoint: {dev_sf_settings.api_address}")
            
        finally:
            # Clean up temporary file
            if os.path.exists(output_file):
                os.unlink(output_file)


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
