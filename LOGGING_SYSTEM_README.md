# 🔧 Professional Logging System for TTS Utility

## 📋 Overview

This professional logging system provides comprehensive request/response tracking, error monitoring, and structured logging for the AudioKit TTS utility. It's designed for production environments with proper log rotation, multiple output formats, and detailed error analysis.

## 🚀 Features

### ✅ **Complete Request Tracking**
- **Request IDs**: Every request gets a unique ID for correlation
- **Timestamps**: Precise timing with millisecond accuracy  
- **Duration Tracking**: Measures request/response times
- **Payload Logging**: Full JSON representation of requests
- **Error Details**: Comprehensive gRPC error capture

### 📊 **Multiple Log Formats**
- **Console Output**: Human-readable progress updates
- **Main Log File**: Detailed structured logs with rotation
- **Error Log**: Dedicated error-only logging
- **JSON Structured**: Machine-readable logs for analysis

### 🔄 **Log Rotation & Management**
- **Automatic Rotation**: 10MB main log, 5MB error log
- **Backup Files**: Keeps 5 main, 3 error backup files
- **UTF-8 Encoding**: Proper handling of Russian text
- **Directory Management**: Creates log directory automatically

## 📁 Log Files Created

| File | Purpose | Size Limit | Backups |
|------|---------|------------|---------|
| `tts_utility.log` | Main detailed logs | 10MB | 5 files |
| `tts_errors.log` | Error-only logs | 5MB | 3 files |
| `tts_structured.jsonl` | JSON structured logs | 20MB | 3 files |

## 🎯 Usage Examples

### **Basic Usage**
```python
from audiogram_client.common_utils.logging_config import init_logging
from audiogram_client.tts.logged_synthesize import LoggedTTSClient

# Initialize logging
logger = init_logging(log_dir="logs", log_level="INFO")

# Use logged TTS client
with LoggedTTSClient("config_audiokit_dev_sf.ini") as client:
    audio = client.synthesize("Test text", voice_name="gandzhaev")
```

### **Advanced Configuration**
```python
# Custom log directory and level
logger = init_logging(log_dir="production_logs", log_level="DEBUG")

# Log custom events
logger.log_system_event("deployment", "New version deployed", {
    "version": "1.2.3",
    "features": ["logging", "error_handling"]
})
```

## 📊 Log Output Examples

### **Console Output**
```
10:04:20 | INFO     | Starting TTS request req_1756883112_0001 to asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443
10:04:22 | ERROR    | Request req_1756883112_0001 failed after 10036.46ms: FutureTimeoutError
```

### **Detailed Log File**
```
2025-09-03 10:04:20 | INFO     | tts_utility | log_request_start:123 | Starting TTS request req_1756883112_0001 to asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443
2025-09-03 10:04:22 | ERROR    | tts_utility | log_request_error:201 | Request req_1756883112_0001 failed after 10036.46ms: 
```

### **JSON Structured Log**
```json
{
  "request_id": "req_1756883112_0001",
  "event": "request_start", 
  "endpoint": "asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443",
  "timestamp": "2025-09-03T10:05:12.918737",
  "auth_present": false,
  "request_data": {
    "text": "Тестирование логирования с ALPN ошибкой",
    "language_code": "ru",
    "encoding": "LINEAR_PCM",
    "sample_rate_hertz": 22050,
    "voice_name": "gandzhaev"
  }
}
```

## 🧪 Testing the System

### **Test ALPN Issue with Logging**
```bash
python test_alpn_with_logs.py
```
This captures the exact ALPN error with full logging context.

### **Full System Test**
```bash
python test_logging_system.py
```
Comprehensive test of all logging features.

## 📈 Production Benefits

### **🔍 Debugging**
- **Request Correlation**: Track requests end-to-end with unique IDs
- **Error Context**: Full stack traces with request context
- **Timing Analysis**: Identify performance bottlenecks

### **📊 Monitoring**
- **Success/Failure Rates**: Track request success patterns
- **Performance Metrics**: Response time analysis
- **Error Patterns**: Identify recurring issues

### **🚨 Alerting**
- **Structured Logs**: Easy parsing for monitoring tools
- **Error Thresholds**: Set up alerts on error rates
- **Performance Monitoring**: Track slow requests

## 🎯 AudioKit Dev SF Integration

The logging system specifically captures:

### **✅ Successful Scenarios**
```json
{
  "event": "request_success",
  "request_id": "req_123",
  "response_size_bytes": 44100,
  "duration_ms": 1250.5
}
```

### **❌ ALPN Errors**
```json
{
  "event": "request_error", 
  "request_id": "req_124",
  "error": {
    "error_type": "FutureTimeoutError",
    "grpc_details": "Cannot check peer: missing selected ALPN property"
  },
  "duration_ms": 10036.46
}
```

### **🔐 Authentication Events**
```json
{
  "event": "auth_token_request",
  "endpoint": "https://isso.mts.ru/auth/",
  "success": true,
  "details": "Token obtained in 245.2ms"
}
```

## 🔧 Configuration

The logging system automatically configures based on:
- **Log Directory**: Specified or defaults to `./logs`
- **Log Level**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **SSL Settings**: From TTS client configuration
- **Endpoints**: Automatically detected from config

## 🎉 Ready for Production

This logging system is enterprise-ready with:
- ✅ **Thread Safety**: Safe for concurrent requests
- ✅ **Error Handling**: Robust exception management  
- ✅ **Performance**: Minimal overhead
- ✅ **Scalability**: Handles high request volumes
- ✅ **Maintenance**: Automatic log rotation
- ✅ **Security**: No sensitive data logged
- ✅ **Standards**: Follows Python logging best practices

Perfect for monitoring AudioKit Dev SF integration and debugging the ALPN issue! 🎯
