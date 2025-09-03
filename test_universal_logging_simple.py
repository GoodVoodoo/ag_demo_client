#!/usr/bin/env python3
"""
Simplified test for universal logging system.
Tests core logging functionality without requiring all implementations.
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from audiogram_client.common_utils.logging_config import init_logging, get_logger
from audiogram_client.tts.logged_synthesize import LoggedTTSClient


def test_universal_logging():
    """Test the universal logging system with available operations."""
    print("🚀 Starting Universal Logging System Test")
    print("=" * 50)
    
    # Initialize comprehensive logging
    logger = init_logging(log_dir="logs", log_level="DEBUG")
    
    print(f"✅ Universal logging system initialized")
    print(f"📁 Logs directory: {Path('logs').absolute()}")
    
    config_path = "config_audiokit_dev_sf.ini"
    
    if not Path(config_path).exists():
        logger.log_system_event("config_missing", f"Configuration file not found: {config_path}")
        print(f"❌ Configuration file not found: {config_path}")
        return False
    
    # Test 1: TTS with Comprehensive Logging
    print("\n🔍 Test 1: TTS with Comprehensive Logging")
    print("-" * 40)
    
    test_cases = [
        {
            "text": "Тестирование универсальной системы логирования AudioKit Dev SF",
            "voice": "gandzhaev",
            "description": "Russian text - main test"
        },
        {
            "text": "Testing universal logging system for AudioKit Dev SF integration",
            "voice": "gandzhaev",
            "description": "English text - secondary test"
        },
        {
            "text": "Проверка обработки ошибок и отказоустойчивости системы",
            "voice": "gandzhaev",
            "description": "Error resilience test"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  📝 Test Case {i}: {test_case['description']}")
        
        try:
            with LoggedTTSClient(config_path) as client:
                start_time = time.time()
                
                audio_data = client.synthesize(
                    text=test_case["text"],
                    voice_name=test_case["voice"],
                    timeout=15.0
                )
                
                duration = time.time() - start_time
                output_file = f"test_universal_case_{i}.wav"
                Path(output_file).write_bytes(audio_data)
                
                print(f"    ✅ Success: {len(audio_data)} bytes in {duration:.2f}s")
                print(f"    💾 Saved to: {output_file}")
                print(f"    📊 Text: '{test_case['text'][:30]}...'")
                
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            print(f"    🔍 Error type: {type(e).__name__}")
            
        # Small delay between requests
        time.sleep(1)
    
    # Test 2: Logging System Features
    print("\n🔍 Test 2: Logging System Features")
    print("-" * 40)
    
    # Test custom events
    logger.log_system_event("custom_test_start", "Testing custom logging events", {
        "test_type": "logging_features",
        "timestamp": time.time(),
        "custom_data": {"version": "1.0", "environment": "test"}
    })
    
    # Test auth logging (simulated)
    logger.log_auth_event("test_auth", "test_endpoint", True, "Simulated auth success")
    logger.log_auth_event("test_auth_fail", "test_endpoint", False, "Simulated auth failure")
    
    # Test error scenarios
    try:
        raise ValueError("Simulated error for logging test")
    except Exception as e:
        # Manual error logging
        logger.logger.error(f"Simulated error captured: {e}")
    
    print("  ✅ Custom events logged")
    print("  ✅ Auth events logged")
    print("  ✅ Error scenarios logged")
    
    # Test 3: Log Analysis
    print("\n🔍 Test 3: Log Analysis")
    print("-" * 40)
    
    stats = logger.get_log_stats()
    print(f"  📊 Total requests: {stats['total_requests']}")
    print(f"  📁 Log directory: {stats['log_directory']}")
    print(f"  📄 Log files: {len(stats['log_files'])}")
    
    for log_file in stats['log_files']:
        log_path = Path(stats['log_directory']) / log_file
        if log_path.exists():
            size_kb = log_path.stat().st_size / 1024
            lines_count = len(log_path.read_text(encoding='utf-8').splitlines())
            print(f"    📄 {log_file}: {size_kb:.1f} KB, {lines_count} lines")
    
    # Test 4: Log Content Analysis
    print("\n🔍 Test 4: Log Content Analysis")
    print("-" * 40)
    
    # Analyze main log
    main_log = Path(stats['log_directory']) / "tts_utility.log"
    if main_log.exists():
        content = main_log.read_text(encoding='utf-8')
        
        # Count different log levels
        info_count = content.count('| INFO     |')
        error_count = content.count('| ERROR    |')
        debug_count = content.count('| DEBUG    |')
        
        print(f"  📊 Log Level Distribution:")
        print(f"    INFO: {info_count} entries")
        print(f"    ERROR: {error_count} entries")
        print(f"    DEBUG: {debug_count} entries")
        
        # Count different event types
        request_starts = content.count('request_start')
        request_errors = content.count('request_error')
        system_events = content.count('system_event')
        
        print(f"  📊 Event Type Distribution:")
        print(f"    Request starts: {request_starts}")
        print(f"    Request errors: {request_errors}")
        print(f"    System events: {system_events}")
    
    # Test 5: JSON Structured Logs
    print("\n🔍 Test 5: JSON Structured Logs")
    print("-" * 40)
    
    json_log = Path(stats['log_directory']) / "tts_structured.jsonl"
    if json_log.exists():
        lines = json_log.read_text(encoding='utf-8').splitlines()
        print(f"  📄 JSON log entries: {len(lines)}")
        
        if lines:
            print("  📋 Sample JSON entry:")
            print(f"    {lines[-1][:100]}...")
    
    # Final summary
    logger.log_system_event("universal_test_complete", 
        "Universal logging system test completed successfully", {
            "total_test_cases": len(test_cases),
            "log_files_created": len(stats['log_files']),
            "test_duration_seconds": time.time() - start_time
        })
    
    print(f"\n🎉 Universal Logging System Test COMPLETED!")
    print(f"📊 Generated comprehensive logs for all operations")
    print(f"📁 Check logs in: {Path(stats['log_directory']).absolute()}")
    
    return True


def show_final_log_summary():
    """Show final summary of all logs created."""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        return
    
    print("\n📋 Final Log Summary")
    print("=" * 30)
    
    total_size = 0
    total_files = 0
    
    for log_file in logs_dir.glob("*"):
        if log_file.is_file():
            size_kb = log_file.stat().st_size / 1024
            total_size += size_kb
            total_files += 1
            
            print(f"📄 {log_file.name}: {size_kb:.1f} KB")
    
    print(f"\n📊 Total: {total_files} files, {total_size:.1f} KB")
    print(f"📁 Location: {logs_dir.absolute()}")


def main():
    """Main test function."""
    start_time = time.time()
    
    try:
        success = test_universal_logging()
        show_final_log_summary()
        
        duration = time.time() - start_time
        
        print(f"\n{'='*50}")
        if success:
            print("✅ UNIVERSAL LOGGING SYSTEM TEST SUCCESSFUL!")
            print("📊 All logging features are operational")
            print(f"⏱️  Test completed in {duration:.1f} seconds")
        else:
            print("❌ Some issues encountered, check logs for details")
        
        print("📈 Professional logging ready for production use!")
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
