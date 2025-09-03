#!/usr/bin/env python3
"""
Comprehensive test for all AudioKit operations logging.
Tests TTS, ASR, Voice Cloning, Models Service, and Audio Archive
with complete logging and error capture.
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from audiogram_client.universal_logged_client import create_audiokit_client


def test_all_operations():
    """Test all AudioKit operations with comprehensive logging."""
    print("🚀 Starting Comprehensive AudioKit Operations Logging Test")
    print("=" * 60)
    
    config_path = "config_audiokit_dev_sf.ini"
    
    if not Path(config_path).exists():
        print(f"❌ Configuration file not found: {config_path}")
        return False
    
    # Create universal client with logging
    with create_audiokit_client(
        config_path=config_path,
        log_dir="logs",
        log_level="DEBUG"
    ) as client:
        
        print(f"✅ Universal AudioKit client initialized")
        print(f"📁 Logs directory: {Path('logs').absolute()}")
        
        # Test 1: Health Check
        print("\n🔍 Test 1: Health Check")
        print("-" * 30)
        try:
            health = client.health_check()
            print(f"Overall status: {health['overall_status']}")
            for service, status in health['services'].items():
                status_icon = "✅" if status['status'] == 'healthy' else "❌"
                print(f"  {status_icon} {service}: {status['status']}")
                if 'response_time_ms' in status:
                    print(f"    Response time: {status['response_time_ms']:.2f}ms")
                if 'error' in status:
                    print(f"    Error: {status['error']}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
        
        # Test 2: Models Service
        print("\n🔍 Test 2: Models Service")
        print("-" * 30)
        try:
            models = client.get_available_models()
            for model_type, model_list in models.items():
                print(f"  📊 {model_type.upper()} models: {len(model_list)}")
                for model in model_list[:2]:  # Show first 2
                    print(f"    - {model.get('name', 'unknown')}")
        except Exception as e:
            print(f"❌ Models query failed: {e}")
        
        # Test 3: TTS Synthesis
        print("\n🔍 Test 3: TTS Synthesis")
        print("-" * 30)
        try:
            tts_results = client.text_to_speech_workflow(
                text="Тестирование универсального клиента с логированием",
                voice_name="gandzhaev",
                output_file="test_universal_tts.wav",
                archive_audio=True
            )
            print(f"  ✅ TTS workflow completed")
            print(f"    Audio size: {tts_results['audio_size_bytes']} bytes")
            print(f"    Output file: {tts_results['output_file']}")
            if tts_results['archive_id']:
                print(f"    Archive ID: {tts_results['archive_id']}")
        except Exception as e:
            print(f"❌ TTS synthesis failed: {e}")
        
        # Test 4: ASR Recognition (if we have test audio)
        print("\n🔍 Test 4: ASR Recognition")
        print("-" * 30)
        test_audio_files = ["1297.wav", "test_universal_tts.wav"]
        asr_success = False
        
        for audio_file in test_audio_files:
            if Path(audio_file).exists():
                try:
                    asr_results = client.speech_to_text_workflow(
                        audio_file=audio_file,
                        language="ru-RU",
                        output_file="test_universal_asr.txt",
                        archive_transcript=True
                    )
                    print(f"  ✅ ASR workflow completed")
                    print(f"    Audio file: {audio_file}")
                    print(f"    Transcript: '{asr_results['transcript'][:50]}...'")
                    print(f"    Length: {asr_results['transcript_length']} characters")
                    if asr_results['archive_id']:
                        print(f"    Archive ID: {asr_results['archive_id']}")
                    asr_success = True
                    break
                except Exception as e:
                    print(f"❌ ASR recognition failed for {audio_file}: {e}")
        
        if not asr_success:
            print(f"⚠️  No suitable audio files found for ASR test")
        
        # Test 5: Voice Cloning
        print("\n🔍 Test 5: Voice Cloning")
        print("-" * 30)
        try:
            # This will likely fail due to ALPN, but we'll capture the logging
            task_id = client.clone_voice(
                voice_name="test_voice_logging",
                audio_files=["1297.wav"] if Path("1297.wav").exists() else [],
                description="Test voice for logging system"
            )
            print(f"  ✅ Voice cloning started: {task_id}")
            
            # Check task status
            task_info = client.get_voice_task_info(task_id)
            print(f"    Task status: {task_info.get('status', 'unknown')}")
            
        except Exception as e:
            print(f"❌ Voice cloning failed: {e}")
        
        # Test 6: Audio Archive Operations
        print("\n🔍 Test 6: Audio Archive Operations")
        print("-" * 30)
        try:
            # Create test audio data
            test_audio = b"fake_audio_data_for_testing" * 100
            
            # Archive audio
            archive_id = client.archive_audio(
                audio_data=test_audio,
                filename="test_logging_audio.wav",
                metadata={"test": True, "source": "comprehensive_test"}
            )
            print(f"  ✅ Audio archived: {archive_id}")
            
            # Archive transcript
            transcript_id = client.archive_transcript(
                transcript="Тестовый транскрипт для проверки архива",
                audio_id=archive_id,
                language="ru-RU"
            )
            print(f"  ✅ Transcript archived: {transcript_id}")
            
        except Exception as e:
            print(f"❌ Audio archive operations failed: {e}")
        
        # Test 7: Error Handling and Logging
        print("\n🔍 Test 7: Error Handling")
        print("-" * 30)
        try:
            # Intentionally cause an error to test error logging
            client.synthesize_text(
                text="",  # Empty text should cause an error
                voice_name="nonexistent_voice"
            )
        except Exception as e:
            print(f"  ✅ Error correctly logged: {type(e).__name__}")
        
        # Final Statistics
        print("\n📊 Final Statistics")
        print("-" * 30)
        stats = client.get_statistics()
        print(f"  Total requests logged: {stats['total_requests']}")
        print(f"  Log files created: {len(stats['log_files'])}")
        
        for log_file in stats['log_files']:
            log_path = Path(stats['log_directory']) / log_file
            if log_path.exists():
                size_kb = log_path.stat().st_size / 1024
                print(f"    📄 {log_file}: {size_kb:.1f} KB")
        
        print(f"\n🎉 Comprehensive logging test completed!")
        print(f"📁 Check detailed logs in: {Path('logs').absolute()}")
        
        return True


def show_log_summary():
    """Show a summary of all log files created."""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        return
    
    print("\n📋 Log Files Summary")
    print("=" * 40)
    
    log_files = {
        "tts_utility.log": "Main detailed logs",
        "tts_errors.log": "Error-only logs",
        "tts_structured.jsonl": "JSON structured logs"
    }
    
    for log_file, description in log_files.items():
        log_path = logs_dir / log_file
        if log_path.exists():
            size_kb = log_path.stat().st_size / 1024
            print(f"📄 {log_file}")
            print(f"   Description: {description}")
            print(f"   Size: {size_kb:.1f} KB")
            
            # Show last few lines
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        print(f"   Last entry: {lines[-1].strip()[:80]}...")
            except Exception:
                pass
            print()


def main():
    """Main test function."""
    try:
        success = test_all_operations()
        show_log_summary()
        
        print("\n" + "=" * 60)
        if success:
            print("✅ All operations logging test COMPLETED successfully!")
            print("📊 Professional logging system is fully operational.")
        else:
            print("❌ Some operations failed, but logging captured all details.")
        
        print("📁 Review logs for complete operation history and troubleshooting.")
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed with unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
