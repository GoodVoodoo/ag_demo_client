#!/usr/bin/env python3
"""
Professional logging system test for TTS utility.
Tests all logging features with real AudioKit Dev SF requests.
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from audiogram_client.common_utils.logging_config import init_logging, get_logger
from audiogram_client.tts.logged_synthesize import LoggedTTSClient, test_logged_synthesis


def main():
    """Test the logging system with AudioKit Dev SF."""
    print("🔧 Initializing TTS Logging System...")
    
    # Initialize logging
    logger = init_logging(log_dir="logs", log_level="DEBUG")
    
    print(f"📁 Log directory: {logger.log_dir}")
    print(f"📊 Log files will be created in: {logger.log_dir.absolute()}")
    
    # Test configuration
    config_path = "config_audiokit_dev_sf.ini"
    
    if not Path(config_path).exists():
        logger.log_system_event("config_missing", f"Configuration file not found: {config_path}")
        print(f"❌ Configuration file not found: {config_path}")
        return False
    
    print(f"⚙️  Using configuration: {config_path}")
    
    # Test 1: Basic logging functionality
    print("\n🧪 Test 1: Basic logging functionality...")
    logger.log_system_event("test_start", "Starting comprehensive logging tests")
    
    # Test 2: Authentication logging
    print("🧪 Test 2: Authentication and connection logging...")
    try:
        with LoggedTTSClient(config_path) as client:
            print("✅ Client initialized successfully")
            
            # Test 3: TTS synthesis with logging
            print("🧪 Test 3: TTS synthesis with full logging...")
            
            test_cases = [
                {
                    "text": "Тестирование системы логирования AudioKit Dev SF",
                    "voice": "gandzhaev",
                    "description": "Russian text with gandzhaev voice"
                },
                {
                    "text": "Testing logging system for AudioKit Dev SF",
                    "voice": "gandzhaev", 
                    "description": "English text with gandzhaev voice"
                }
            ]
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"  📝 Test case {i}: {test_case['description']}")
                
                try:
                    start_time = time.time()
                    audio_data = client.synthesize(
                        text=test_case["text"],
                        voice_name=test_case["voice"],
                        timeout=10.0
                    )
                    duration = time.time() - start_time
                    
                    # Save test audio
                    output_file = f"test_logged_case_{i}.wav"
                    Path(output_file).write_bytes(audio_data)
                    
                    print(f"    ✅ Success: {len(audio_data)} bytes in {duration:.2f}s")
                    print(f"    💾 Saved to: {output_file}")
                    
                except Exception as e:
                    print(f"    ❌ Failed: {e}")
                    
                # Small delay between requests
                time.sleep(1)
    
    except Exception as e:
        print(f"❌ Client error: {e}")
    
    # Test 4: Log analysis
    print("\n🧪 Test 4: Log file analysis...")
    stats = logger.get_log_stats()
    print(f"📊 Logging statistics:")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Log files created: {len(stats['log_files'])}")
    
    for log_file in stats['log_files']:
        log_path = logger.log_dir / log_file
        if log_path.exists():
            size_kb = log_path.stat().st_size / 1024
            print(f"    📄 {log_file}: {size_kb:.1f} KB")
    
    # Display recent log entries
    print("\n📋 Recent log entries:")
    main_log = logger.log_dir / "tts_utility.log"
    if main_log.exists():
        try:
            with open(main_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-10:]  # Last 10 lines
                for line in lines:
                    print(f"  {line.rstrip()}")
        except Exception as e:
            print(f"  ⚠️  Could not read log file: {e}")
    
    print("\n✅ Logging system test completed!")
    print(f"📁 Check logs in: {logger.log_dir.absolute()}")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
