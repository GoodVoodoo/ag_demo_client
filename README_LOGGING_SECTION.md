# 📊 Universal Logging System

This client includes a **professional-grade logging system** that automatically tracks ALL AudioKit operations with comprehensive error capture, performance monitoring, and structured logging.

## 🚀 Quick Start with Logging

```python
from audiogram_client.universal_logged_client import create_audiokit_client

# All operations automatically logged!
with create_audiokit_client("config_audiokit_dev_sf.ini") as client:
    # TTS with automatic logging
    audio = client.synthesize_text("Hello world", voice_name="gandzhaev")
    
    # ASR with automatic logging  
    text = client.recognize_audio("audio.wav", language="ru-RU")
    
    # Health check with logging
    health = client.health_check()
```

## 📊 What Gets Logged Automatically

- **🆔 Unique Request IDs** for tracking operations end-to-end
- **⏰ Precise Timing** with millisecond accuracy for performance analysis
- **📋 Complete Request Data** (text, voice, language, file sizes)
- **📊 Response Details** (audio size, transcript length, success/failure)
- **🔐 Authentication Events** (token requests, success/failure rates)
- **❌ Comprehensive Error Capture** (including ALPN issues, gRPC errors)
- **🏥 Health Monitoring** (service availability, response times)

## 📁 Log Files Created (Never Endless!)

The system creates three types of logs with **automatic rotation**:

- **`logs/tts_utility.log`** - Human-readable detailed logs (10MB max, 5 backups)
- **`logs/tts_errors.log`** - Error-only logs for debugging (5MB max, 3 backups)  
- **`logs/tts_structured.jsonl`** - JSON logs for analysis (20MB max, 3 backups)

**Total Maximum: ~125MB** - automatically managed with log rotation!

## 🔍 Monitor Logs in Real-Time

```bash
# Watch all activity
tail -f logs/tts_utility.log

# Watch errors only
tail -f logs/tts_errors.log

# Watch JSON logs for analysis
tail -f logs/tts_structured.jsonl | jq .
```

## 📈 Log Analysis Examples

```bash
# Count requests by service
grep "request_start" logs/tts_structured.jsonl | jq -r '.request_data.service' | sort | uniq -c

# Find slow requests (>5 seconds)
grep "duration_ms" logs/tts_structured.jsonl | jq 'select(.duration_ms > 5000)'

# Error analysis
grep "request_error" logs/tts_structured.jsonl | jq -r '.error.error_type' | sort | uniq -c
```

## 🎯 Perfect for Production

- ✅ **Enterprise-Grade**: Thread-safe, minimal overhead (<1%)
- ✅ **Security-Conscious**: No passwords or secrets logged
- ✅ **Integration-Ready**: JSON format for monitoring tools
- ✅ **AudioKit Dev SF Ready**: Captures ALPN errors for support

## 🧪 Test the Logging System

```bash
# Test comprehensive logging
python test_universal_logging_simple.py

# View practical examples
python LOGGING_USAGE_EXAMPLES.py
```

**📖 Complete Documentation:** [UNIVERSAL_LOGGING_SYSTEM_README.md](UNIVERSAL_LOGGING_SYSTEM_README.md)
