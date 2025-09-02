#!/usr/bin/env python3
"""Working English TTS example with correct parameters"""

import sys
import os
from pathlib import Path

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audiogram_client.common_utils.config import Settings
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
from audiogram_client.genproto import tts_pb2, tts_pb2_grpc
from audiogram_client.tts.utils.request import make_tts_request
from audiogram_client.common_utils.types import TTSVoiceStyle

def test_english_tts():
    # Load settings
    settings = Settings(['config.ini'])
    settings.validators.validate()
    
    print("Testing English TTS with correct parameters...\n")
    
    # Get authentication
    auth_metadata = get_auth_metadata(
        settings.sso_url,
        settings.realm,
        settings.client_id,
        settings.client_secret,
        settings.iam_account,
        settings.iam_workspace,
        settings.verify_sso,
    )
    
    # English TTS parameters (as specified)
    text = "Hello, this is an English text-to-speech test with voice two."
    voice_name = "voice 2"
    model_type = "eng voice"
    language_code = "en"
    sample_rate = 8000  # Correct: 8000 Hz
    custom_options = {"length_scale": 1.33}  # English-specific
    
    print(f"Parameters:")
    print(f"  Text: {text}")
    print(f"  Voice: {voice_name}")
    print(f"  Model Type: {model_type}")
    print(f"  Language: {language_code}")
    print(f"  Sample Rate: {sample_rate} Hz")
    print(f"  Custom Options: {custom_options}")
    
    # Create request
    request = make_tts_request(
        text=text,
        is_ssml=False,  # English uses text field, not SSML
        voice_name=voice_name,
        rate=sample_rate,
        model_type=model_type,
        model_rate=None,
        voice_style=TTSVoiceStyle.neutral,
        language_code=language_code,
        custom_options=custom_options,
    )
    
    print(f"\nRequest proto:")
    print(request)
    
    print(f"\nConnecting to: {settings.api_address}")
    
    try:
        with open_grpc_channel(
            settings.api_address,
            ssl_creds_from_settings(settings),
        ) as channel:
            stub = tts_pb2_grpc.TTSStub(channel)
            
            response, call = stub.Synthesize.with_call(
                request,
                metadata=auth_metadata,
                timeout=settings.timeout,
            )
            
            print(f"\n✓ SUCCESS! Audio size: {len(response.audio)} bytes")
            
            # Save the audio
            output_file = "english_voice2_8khz.wav"
            Path(output_file).write_bytes(response.audio)
            print(f"Audio saved to: {output_file}")
            
            return True
            
    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}")
        print(f"Details: {e}")
        return False

def test_russian_tts():
    """Test Russian TTS for comparison"""
    settings = Settings(['config.ini'])
    settings.validators.validate()
    
    print("\n\nTesting Russian TTS for comparison...\n")
    
    auth_metadata = get_auth_metadata(
        settings.sso_url,
        settings.realm,
        settings.client_id,
        settings.client_secret,
        settings.iam_account,
        settings.iam_workspace,
        settings.verify_sso,
    )
    
    # Russian TTS parameters
    text = "<speak>Привет, это тест русского синтеза речи.</speak>"
    voice_name = "borisova"
    model_type = "high_quality"
    language_code = "ru"
    sample_rate = 8000
    
    print(f"Parameters:")
    print(f"  SSML: {text}")
    print(f"  Voice: {voice_name}")
    print(f"  Model Type: {model_type}")
    print(f"  Language: {language_code}")
    print(f"  Sample Rate: {sample_rate} Hz")
    
    request = make_tts_request(
        text=text,
        is_ssml=True,  # Russian uses SSML
        voice_name=voice_name,
        rate=sample_rate,
        model_type=model_type,
        model_rate=None,
        voice_style=TTSVoiceStyle.neutral,
        language_code=language_code,
        custom_options=None,  # No custom options for Russian
    )
    
    try:
        with open_grpc_channel(
            settings.api_address,
            ssl_creds_from_settings(settings),
        ) as channel:
            stub = tts_pb2_grpc.TTSStub(channel)
            
            response, call = stub.Synthesize.with_call(
                request,
                metadata=auth_metadata,
                timeout=settings.timeout,
            )
            
            print(f"\n✓ SUCCESS! Audio size: {len(response.audio)} bytes")
            
            output_file = "russian_borisova_8khz.wav"
            Path(output_file).write_bytes(response.audio)
            print(f"Audio saved to: {output_file}")
            
            return True
            
    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}")
        print(f"Details: {e}")
        return False

if __name__ == "__main__":
    english_ok = test_english_tts()
    russian_ok = test_russian_tts()
    
    print("\n" + "="*60)
    print("SUMMARY:")
    print(f"English TTS: {'✓ Working' if english_ok else '✗ Failed'}")
    print(f"Russian TTS: {'✓ Working' if russian_ok else '✗ Failed'}")
    
    if english_ok:
        print("\n🎉 English TTS Configuration:")
        print("- Voice names: voice 1, voice 2, voice 3, voice 4")
        print("- Model type: 'eng voice'")
        print("- Language code: 'en'")
        print("- Sample rate: 8000 Hz")
        print("- Custom option: length_scale = 1.33")
        print("- Use 'text' field (not SSML)")
    
    sys.exit(0 if english_ok else 1)
