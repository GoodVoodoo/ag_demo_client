"""
Professional logging configuration for AudioKit TTS utility.
Provides structured logging with request/response tracking, error handling,
and proper log rotation for production environments.
"""

import logging
import logging.handlers
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import grpc
from google.protobuf.json_format import MessageToJson


class TTSLogger:
    """Professional logging system for TTS utility operations."""
    
    def __init__(self, log_dir: str = "logs", log_level: str = "INFO"):
        """
        Initialize the TTS logging system.
        
        Args:
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Set up main logger
        self.logger = logging.getLogger("tts_utility")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Set up formatters
        self._setup_formatters()
        
        # Set up handlers
        self._setup_handlers()
        
        # Request tracking
        self.request_counter = 0
        
    def _setup_formatters(self):
        """Set up log formatters for different output types."""
        # Detailed formatter for file logs
        self.detailed_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # JSON formatter for structured logs
        self.json_formatter = logging.Formatter(
            fmt='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "function": "%(funcName)s", "line": %(lineno)d, "message": %(message)s}',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console formatter (simplified)
        self.console_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
    
    def _setup_handlers(self):
        """Set up log handlers for console and file output."""
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(console_handler)
        
        # Main log file with rotation (10MB, keep 5 files)
        main_log_handler = logging.handlers.RotatingFileHandler(
            filename=self.log_dir / "tts_utility.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        main_log_handler.setLevel(logging.DEBUG)
        main_log_handler.setFormatter(self.detailed_formatter)
        self.logger.addHandler(main_log_handler)
        
        # Error log file (errors only)
        error_log_handler = logging.handlers.RotatingFileHandler(
            filename=self.log_dir / "tts_errors.log",
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_log_handler.setLevel(logging.ERROR)
        error_log_handler.setFormatter(self.detailed_formatter)
        self.logger.addHandler(error_log_handler)
        
        # Structured JSON log for analysis
        json_log_handler = logging.handlers.RotatingFileHandler(
            filename=self.log_dir / "tts_structured.jsonl",
            maxBytes=20 * 1024 * 1024,  # 20MB
            backupCount=3,
            encoding='utf-8'
        )
        json_log_handler.setLevel(logging.INFO)
        json_log_handler.setFormatter(self.json_formatter)
        self.logger.addHandler(json_log_handler)
    
    def log_request_start(self, endpoint: str, request_data: Any, 
                         auth_present: bool = False) -> str:
        """
        Log the start of a TTS request.
        
        Args:
            endpoint: Target endpoint
            request_data: Request protobuf or dict
            auth_present: Whether authentication is present
            
        Returns:
            Request ID for correlation
        """
        self.request_counter += 1
        request_id = f"req_{int(time.time())}_{self.request_counter:04d}"
        
        # Convert protobuf to dict if needed
        if hasattr(request_data, 'SerializeToString'):
            try:
                request_dict = json.loads(MessageToJson(request_data, preserving_proto_field_name=True))
            except Exception:
                request_dict = {"error": "Failed to serialize protobuf", "size": len(request_data.SerializeToString())}
        else:
            request_dict = request_data
        
        log_data = {
            "request_id": request_id,
            "event": "request_start",
            "endpoint": endpoint,
            "timestamp": datetime.now().isoformat(),
            "auth_present": auth_present,
            "request_data": request_dict
        }
        
        self.logger.info(json.dumps(log_data, ensure_ascii=False))
        self.logger.info(f"Starting TTS request {request_id} to {endpoint}")
        
        return request_id
    
    def log_request_success(self, request_id: str, response_size: int = 0, 
                           duration_ms: float = 0):
        """
        Log successful TTS request completion.
        
        Args:
            request_id: Request correlation ID
            response_size: Size of response in bytes
            duration_ms: Request duration in milliseconds
        """
        log_data = {
            "request_id": request_id,
            "event": "request_success",
            "timestamp": datetime.now().isoformat(),
            "response_size_bytes": response_size,
            "duration_ms": duration_ms
        }
        
        self.logger.info(json.dumps(log_data, ensure_ascii=False))
        self.logger.info(f"Request {request_id} completed successfully - {response_size} bytes in {duration_ms:.2f}ms")
    
    def log_request_error(self, request_id: str, error: Exception, 
                         duration_ms: float = 0):
        """
        Log TTS request error.
        
        Args:
            request_id: Request correlation ID
            error: Exception that occurred
            duration_ms: Request duration in milliseconds
        """
        # Extract gRPC error details
        error_details = {
            "error_type": type(error).__name__,
            "error_message": str(error)
        }
        
        if isinstance(error, grpc.RpcError):
            error_details.update({
                "grpc_code": str(error.code()),
                "grpc_details": error.details() if hasattr(error, 'details') else None,
                "grpc_debug": getattr(error, 'debug_error_string', lambda: None)()
            })
        
        log_data = {
            "request_id": request_id,
            "event": "request_error",
            "timestamp": datetime.now().isoformat(),
            "duration_ms": duration_ms,
            "error": error_details
        }
        
        self.logger.error(json.dumps(log_data, ensure_ascii=False))
        self.logger.error(f"Request {request_id} failed after {duration_ms:.2f}ms: {error}")
    
    def log_system_event(self, event_type: str, message: str, data: Dict[str, Any] = None):
        """
        Log system-level events.
        
        Args:
            event_type: Type of event (startup, shutdown, config_change, etc.)
            message: Human-readable message
            data: Additional structured data
        """
        log_data = {
            "event": f"system_{event_type}",
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "data": data or {}
        }
        
        self.logger.info(json.dumps(log_data, ensure_ascii=False))
        self.logger.info(f"System event: {message}")
    
    def log_auth_event(self, event_type: str, endpoint: str, success: bool, 
                      details: str = ""):
        """
        Log authentication-related events.
        
        Args:
            event_type: Type of auth event (token_request, token_refresh, etc.)
            endpoint: Authentication endpoint
            success: Whether auth was successful
            details: Additional details
        """
        log_data = {
            "event": f"auth_{event_type}",
            "timestamp": datetime.now().isoformat(),
            "endpoint": endpoint,
            "success": success,
            "details": details
        }
        
        level = logging.INFO if success else logging.ERROR
        self.logger.log(level, json.dumps(log_data, ensure_ascii=False))
        
        status = "succeeded" if success else "failed"
        self.logger.log(level, f"Authentication {event_type} {status} for {endpoint}: {details}")
    
    def get_log_stats(self) -> Dict[str, Any]:
        """Get logging statistics."""
        return {
            "log_directory": str(self.log_dir),
            "total_requests": self.request_counter,
            "log_files": [f.name for f in self.log_dir.glob("*.log*")],
            "current_time": datetime.now().isoformat()
        }


# Global logger instance
_tts_logger: Optional[TTSLogger] = None


def get_logger() -> TTSLogger:
    """Get the global TTS logger instance."""
    global _tts_logger
    if _tts_logger is None:
        _tts_logger = TTSLogger()
    return _tts_logger


def init_logging(log_dir: str = "logs", log_level: str = "INFO") -> TTSLogger:
    """
    Initialize the global logging system.
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level
        
    Returns:
        Configured logger instance
    """
    global _tts_logger
    _tts_logger = TTSLogger(log_dir, log_level)
    _tts_logger.log_system_event("startup", "TTS logging system initialized", {
        "log_dir": log_dir,
        "log_level": log_level
    })
    return _tts_logger
