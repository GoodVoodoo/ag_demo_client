#!/usr/bin/env python3
"""
Practical examples showing how to use the universal logging system.
Demonstrates all services with real-world scenarios.
"""

import time
import json
from pathlib import Path

# Import the universal logging system
from audiogram_client.universal_logged_client import create_audiokit_client
from audiogram_client.common_utils.logging_config import init_logging, get_logger

# Individual service imports for advanced usage
from audiogram_client.tts.logged_synthesize import LoggedTTSClient
from audiogram_client.asr.logged_recognize import LoggedASRClient
from audiogram_client.voice_cloning.logged_clone import LoggedVoiceCloningClient
from audiogram_client.models.logged_service import LoggedModelsClient
from audiogram_client.audio_archive.logged_archive import LoggedAudioArchiveClient


def example_1_basic_usage():
    """Example 1: Basic usage with universal client"""
    print("🔧 Example 1: Basic Universal Client Usage")
    print("-" * 50)
    
    # Create universal client with logging
    with create_audiokit_client(
        config_path="config_audiokit_dev_sf.ini",
        log_dir="examples_logs",
        log_level="INFO"
    ) as client:
        
        try:
            # TTS - Simple text synthesis
            print("  🗣️ Testing TTS...")
            audio_data = client.synthesize_text(
                text="Пример использования системы логирования",
                voice_name="gandzhaev",
                save_to="example_basic.wav"
            )
            print(f"    ✅ Generated {len(audio_data)} bytes of audio")
            
            # Health check
            print("  🏥 Testing Health Check...")
            health = client.health_check()
            print(f"    📊 Overall status: {health['overall_status']}")
            
            # Models query
            print("  📊 Testing Models Query...")
            models = client.get_available_models()
            total_models = sum(len(model_list) for model_list in models.values())
            print(f"    📈 Found {total_models} total models")
            
        except Exception as e:
            print(f"    ❌ Error (logged automatically): {e}")


def example_2_tts_workflows():
    """Example 2: TTS workflows with archiving"""
    print("\n🗣️ Example 2: TTS Workflows")
    print("-" * 50)
    
    with create_audiokit_client("config_audiokit_dev_sf.ini", log_level="DEBUG") as client:
        
        # Simple TTS workflow
        try:
            print("  📝 Simple TTS workflow...")
            result = client.text_to_speech_workflow(
                text="Это пример простого рабочего процесса TTS",
                voice_name="gandzhaev",
                output_file="workflow_simple.wav",
                archive_audio=False
            )
            print(f"    ✅ Workflow ID: {result['workflow_id']}")
            print(f"    📄 Output file: {result['output_file']}")
            
        except Exception as e:
            print(f"    ❌ Workflow failed: {e}")
        
        # Advanced TTS workflow with archiving
        try:
            print("  📝 Advanced TTS workflow with archiving...")
            result = client.text_to_speech_workflow(
                text="Это пример расширенного рабочего процесса с архивированием",
                voice_name="gandzhaev",
                output_file="workflow_advanced.wav",
                archive_audio=True
            )
            print(f"    ✅ Workflow ID: {result['workflow_id']}")
            print(f"    📁 Archive ID: {result['archive_id']}")
            
        except Exception as e:
            print(f"    ❌ Advanced workflow failed: {e}")


def example_3_individual_services():
    """Example 3: Using individual service clients"""
    print("\n🔧 Example 3: Individual Service Clients")
    print("-" * 50)
    
    config_path = "config_audiokit_dev_sf.ini"
    
    # TTS Client
    print("  🗣️ Individual TTS Client...")
    try:
        with LoggedTTSClient(config_path) as tts:
            audio = tts.synthesize(
                text="Индивидуальный клиент TTS",
                voice_name="gandzhaev",
                timeout=10.0
            )
            print(f"    ✅ TTS: {len(audio)} bytes generated")
    except Exception as e:
        print(f"    ❌ TTS failed: {e}")
    
    # Models Client
    print("  📊 Individual Models Client...")
    try:
        with LoggedModelsClient(config_path) as models:
            tts_models = models.get_tts_models()
            print(f"    ✅ Models: {len(tts_models)} TTS models available")
    except Exception as e:
        print(f"    ❌ Models query failed: {e}")
    
    # Voice Cloning Client (will likely fail due to ALPN, but logs the attempt)
    print("  🎤 Individual Voice Cloning Client...")
    try:
        with LoggedVoiceCloningClient(config_path) as vc:
            # This will demonstrate error logging
            task_id = vc.clone_voice(
                voice_name="example_voice",
                audio_files=["example.wav"] if Path("example.wav").exists() else [],
                description="Example voice cloning"
            )
            print(f"    ✅ Voice Cloning: Task {task_id} started")
    except Exception as e:
        print(f"    ❌ Voice Cloning failed: {e}")


def example_4_custom_logging():
    """Example 4: Custom logging events"""
    print("\n📝 Example 4: Custom Logging Events")
    print("-" * 50)
    
    # Initialize logging and get logger
    logger = init_logging(log_dir="examples_logs", log_level="INFO")
    
    # Custom system events
    print("  📋 Logging custom system events...")
    logger.log_system_event("user_session_start", "User started audio processing session", {
        "user_id": "user_123",
        "session_type": "batch_processing",
        "estimated_files": 10,
        "start_time": time.time()
    })
    
    logger.log_system_event("batch_job_progress", "Batch processing update", {
        "job_id": "batch_001",
        "completed": 3,
        "total": 10,
        "progress_percent": 30
    })
    
    # Custom authentication events
    print("  🔐 Logging custom auth events...")
    logger.log_auth_event("api_key_validation", "api.audiokit.dev", True, 
                         "API key validated for premium features")
    
    logger.log_auth_event("token_refresh", "auth.audiokit.dev", False,
                         "Token refresh failed - expired refresh token")
    
    # Custom workflow events
    print("  🔄 Logging custom workflow events...")
    logger.log_system_event("workflow_complete", "Audio processing workflow finished", {
        "workflow_id": "wf_20240115_001",
        "input_files": 5,
        "output_files": 5,
        "total_duration_seconds": 245,
        "total_audio_mb": 15.7,
        "success_rate": 100
    })
    
    print("    ✅ Custom events logged successfully")


def example_5_log_analysis():
    """Example 5: Analyzing logs programmatically"""
    print("\n📊 Example 5: Log Analysis")
    print("-" * 50)
    
    # Analyze JSON logs
    json_log_path = Path("examples_logs/tts_structured.jsonl")
    
    if not json_log_path.exists():
        print("    ⚠️ No JSON logs found. Run other examples first.")
        return
    
    print("  📋 Analyzing structured logs...")
    
    # Parse logs
    requests = []
    errors = []
    auth_events = []
    system_events = []
    
    with open(json_log_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line)
                
                if 'request_id' in entry:
                    requests.append(entry)
                    if entry.get('event') == 'request_error':
                        errors.append(entry)
                
                if entry.get('event', '').startswith('auth_'):
                    auth_events.append(entry)
                
                if entry.get('event', '').startswith('system_'):
                    system_events.append(entry)
                    
            except json.JSONDecodeError:
                continue
    
    # Analysis results
    print(f"    📊 Analysis Results:")
    print(f"      Total requests: {len(requests)}")
    print(f"      Errors: {len(errors)}")
    if requests:
        success_rate = ((len(requests) - len(errors)) / len(requests)) * 100
        print(f"      Success rate: {success_rate:.1f}%")
    
    print(f"      Auth events: {len(auth_events)}")
    print(f"      System events: {len(system_events)}")
    
    # Service breakdown
    services = {}
    for req in requests:
        service = req.get('request_data', {}).get('service', 'unknown')
        services[service] = services.get(service, 0) + 1
    
    if services:
        print(f"      Services used:")
        for service, count in services.items():
            print(f"        {service}: {count} requests")
    
    # Error analysis
    if errors:
        print(f"      Error types:")
        error_types = {}
        for error in errors:
            error_type = error.get('error', {}).get('error_type', 'unknown')
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        for error_type, count in error_types.items():
            print(f"        {error_type}: {count} occurrences")


def example_6_monitoring_setup():
    """Example 6: Setting up real-time monitoring"""
    print("\n🔍 Example 6: Monitoring Setup")
    print("-" * 50)
    
    print("  📈 Real-time monitoring commands:")
    print("    # Monitor all activity:")
    print("    tail -f examples_logs/tts_utility.log")
    print()
    print("    # Monitor errors only:")
    print("    tail -f examples_logs/tts_errors.log")
    print()
    print("    # Monitor JSON logs with formatting:")
    print("    tail -f examples_logs/tts_structured.jsonl | jq .")
    print()
    print("    # Monitor specific service:")
    print("    tail -f examples_logs/tts_utility.log | grep 'TTS\\|request_start'")
    print()
    
    print("  📊 Log analysis commands:")
    print("    # Count requests by service:")
    print("    grep 'request_start' examples_logs/tts_structured.jsonl | jq -r '.request_data.service' | sort | uniq -c")
    print()
    print("    # Find slow requests (>5 seconds):")
    print("    grep 'duration_ms' examples_logs/tts_structured.jsonl | jq 'select(.duration_ms > 5000)'")
    print()
    print("    # Error analysis:")
    print("    grep 'request_error' examples_logs/tts_structured.jsonl | jq -r '.error.error_type' | sort | uniq -c")
    
    # Show current log statistics
    logger = get_logger()
    stats = logger.get_log_stats()
    
    print("\n  📁 Current log statistics:")
    print(f"    Log directory: {stats['log_directory']}")
    print(f"    Total requests logged: {stats['total_requests']}")
    print(f"    Log files: {len(stats['log_files'])}")
    
    for log_file in stats['log_files']:
        log_path = Path(stats['log_directory']) / log_file
        if log_path.exists():
            size_kb = log_path.stat().st_size / 1024
            print(f"      📄 {log_file}: {size_kb:.1f} KB")


def main():
    """Run all examples"""
    print("🚀 Universal Logging System - Usage Examples")
    print("=" * 60)
    
    # Run examples
    example_1_basic_usage()
    example_2_tts_workflows()
    example_3_individual_services()
    example_4_custom_logging()
    example_5_log_analysis()
    example_6_monitoring_setup()
    
    print("\n" + "=" * 60)
    print("✅ All examples completed!")
    print("📁 Check examples_logs/ directory for generated logs")
    print("📖 Review UNIVERSAL_LOGGING_SYSTEM_README.md for detailed documentation")


if __name__ == "__main__":
    main()
