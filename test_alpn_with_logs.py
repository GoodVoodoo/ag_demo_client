#!/usr/bin/env python3
"""
Test ALPN issue with comprehensive logging.
Demonstrates the professional logging system while capturing the exact ALPN error.
"""

import sys
import time
import grpc
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from audiogram_client.common_utils.logging_config import init_logging, get_logger
from audiogram_client.common_utils.config import Settings
from audiogram_client.tts.utils.request import make_tts_request
from audiogram_client.genproto.tts_pb2_grpc import TTSStub
from audiogram_client.common_utils.types import TTSVoiceStyle


def test_alpn_with_logging():
    """Test the ALPN issue with full logging capture."""
    print("🔧 Initializing Professional Logging System...")
    
    # Initialize logging
    logger = init_logging(log_dir="logs", log_level="DEBUG")
    
    print(f"📁 Logs will be saved to: {logger.log_dir.absolute()}")
    
    # Load config
    config_path = "config_audiokit_dev_sf.ini"
    
    if not Path(config_path).exists():
        logger.log_system_event("config_missing", f"Configuration file not found: {config_path}")
        print(f"❌ Configuration file not found: {config_path}")
        return False
    
    logger.log_system_event("test_start", "Starting ALPN error capture with logging", {
        "config_path": config_path,
        "target": "AudioKit Dev SF"
    })
    
    try:
        # Load settings
        settings = Settings([config_path])
        
        logger.log_system_event("config_loaded", "Configuration loaded successfully", {
            "endpoint": settings.api_address,
            "ssl_enabled": settings.use_ssl,
            "ca_cert": settings.ca_cert_path if settings.ca_cert_path else "system_store"
        })
        
        print(f"🎯 Target endpoint: {settings.api_address}")
        
        # Create TTS request
        request = make_tts_request(
            text="Тестирование логирования с ALPN ошибкой",
            is_ssml=False,
            voice_name="gandzhaev",
            rate=22050,
            model_type=None,
            model_rate=None,
            voice_style=TTSVoiceStyle.neutral
        )
        
        # Log request start
        request_id = logger.log_request_start(
            endpoint=settings.api_address,
            request_data=request,
            auth_present=False  # We'll skip auth to focus on ALPN
        )
        
        print(f"📡 Starting request {request_id}...")
        
        # Attempt gRPC connection
        start_time = time.time()
        
        try:
            # Create channel
            if settings.use_ssl:
                creds = grpc.ssl_channel_credentials(
                    root_certificates=None,  # Use system trust store
                    private_key=None,
                    certificate_chain=None
                )
                channel = grpc.secure_channel(settings.api_address, creds)
            else:
                channel = grpc.insecure_channel(settings.api_address)
            
            logger.log_system_event("channel_created", "gRPC channel created", {
                "ssl_enabled": settings.use_ssl,
                "request_id": request_id
            })
            
            # Test channel readiness (this will fail with ALPN error)
            stub = TTSStub(channel)
            future = grpc.channel_ready_future(channel)
            future.result(timeout=10)
            
            # If we get here, connection worked (unexpected)
            duration_ms = (time.time() - start_time) * 1000
            logger.log_request_success(request_id, 0, duration_ms)
            print("✅ Unexpected success - ALPN issue may be resolved!")
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log the exact error
            logger.log_request_error(request_id, e, duration_ms)
            
            print(f"❌ Expected ALPN error captured:")
            print(f"   Error type: {type(e).__name__}")
            print(f"   Duration: {duration_ms:.2f}ms")
            
            if hasattr(e, 'details'):
                print(f"   Details: {e.details()}")
            
            print(f"   Full error: {e}")
            
        finally:
            try:
                channel.close()
            except:
                pass
    
    except Exception as e:
        logger.log_system_event("test_failed", f"Test setup failed: {e}", {
            "error": str(e),
            "error_type": type(e).__name__
        })
        print(f"❌ Test setup failed: {e}")
        return False
    
    # Show log summary
    print("\n📊 Logging Summary:")
    stats = logger.get_log_stats()
    print(f"  Total requests logged: {stats['total_requests']}")
    print(f"  Log files created: {len(stats['log_files'])}")
    
    for log_file in stats['log_files']:
        log_path = logger.log_dir / log_file
        if log_path.exists():
            size_kb = log_path.stat().st_size / 1024
            print(f"    📄 {log_file}: {size_kb:.1f} KB")
    
    # Show the structured log entry for the error
    print("\n📋 Structured Error Log (JSON):")
    json_log = logger.log_dir / "tts_structured.jsonl"
    if json_log.exists():
        try:
            with open(json_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    print(f"  {lines[-1].strip()}")  # Last line
        except Exception:
            print("  (Could not read structured log)")
    
    logger.log_system_event("test_complete", "ALPN error logging test completed successfully")
    
    print(f"\n✅ Professional logging system demonstrated!")
    print(f"📁 All logs saved to: {logger.log_dir.absolute()}")
    print(f"📊 Logs include: timestamps, request IDs, error details, and structured JSON")
    
    return True


if __name__ == "__main__":
    success = test_alpn_with_logging()
    sys.exit(0 if success else 1)
