"""
ASR (Speech Recognition) with professional logging integration.
Wraps the standard ASR recognition with comprehensive request/response logging.
"""

import time
import grpc
from pathlib import Path
from typing import Optional, Iterator, Union

from audiogram_client.common_utils.logging_config import get_logger
from audiogram_client.common_utils.config import Settings
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.connection import create_channel
from audiogram_client.asr.utils.request import make_streaming_recognize_request
from audiogram_client.genproto.stt_pb2_grpc import STTStub
from audiogram_client.genproto.stt_pb2 import RecognizeResponse


class LoggedASRClient:
    """ASR client with comprehensive logging capabilities."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize logged ASR client.
        
        Args:
            config_path: Path to configuration file
        """
        self.logger = get_logger()
        self.settings = Settings([config_path] if config_path else [])
        self.channel = None
        self.stub = None
        
        # Log client initialization
        self.logger.log_system_event("asr_client_init", "ASR client initialized", {
            "config_path": config_path,
            "endpoint": self.settings.api_address,
            "ssl_enabled": self.settings.use_ssl
        })
    
    def _ensure_connection(self):
        """Ensure gRPC connection is established."""
        if self.channel is None:
            start_time = time.time()
            try:
                self.channel = create_channel(self.settings)
                self.stub = STTStub(self.channel)
                
                # Test connection
                future = grpc.channel_ready_future(self.channel)
                future.result(timeout=10)
                
                duration = (time.time() - start_time) * 1000
                self.logger.log_system_event("asr_connection_established", 
                    "ASR gRPC channel established successfully", {
                        "endpoint": self.settings.api_address,
                        "duration_ms": duration
                    })
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                self.logger.log_system_event("asr_connection_failed",
                    f"Failed to establish ASR gRPC channel: {e}", {
                        "endpoint": self.settings.api_address,
                        "duration_ms": duration,
                        "error": str(e)
                    })
                raise
    
    def _get_auth_metadata(self) -> list:
        """Get authentication metadata with logging."""
        try:
            start_time = time.time()
            metadata = get_auth_metadata(
                sso_url=self.settings.sso_url,
                realm=self.settings.realm,
                client_id=self.settings.client_id,
                client_secret=self.settings.client_secret,
                iam_account=getattr(self.settings, 'iam_account', ''),
                iam_workspace=getattr(self.settings, 'iam_workspace', ''),
                verify_sso=self.settings.verify_sso
            )
            duration = (time.time() - start_time) * 1000
            
            self.logger.log_auth_event("asr_token_request", self.settings.sso_url, 
                                     True, f"ASR auth metadata obtained in {duration:.2f}ms")
            
            return metadata
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.logger.log_auth_event("asr_token_request", self.settings.sso_url,
                                     False, f"ASR auth request failed after {duration:.2f}ms: {e}")
            raise
    
    def recognize_file(self, audio_file_path: str, language: str = "ru-RU", 
                      model: Optional[str] = None, sample_rate: int = 16000,
                      timeout: float = 60.0) -> str:
        """
        Recognize speech from audio file with comprehensive logging.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (e.g., "ru-RU", "en-US")
            model: ASR model to use
            sample_rate: Audio sample rate
            timeout: Request timeout in seconds
            
        Returns:
            Recognized text
            
        Raises:
            Exception: If recognition fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Read audio file
        audio_path = Path(audio_file_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        audio_data = audio_path.read_bytes()
        
        # Create request
        request = make_streaming_recognize_request(
            audio_data=audio_data,
            language=language,
            model=model,
            sample_rate=sample_rate
        )
        
        # Get auth metadata
        metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "audio_file": audio_file_path,
                "audio_size_bytes": len(audio_data),
                "language": language,
                "model": model or "default",
                "sample_rate": sample_rate,
                "service": "ASR_Recognize"
            },
            auth_present=bool(metadata)
        )
        
        start_time = time.time()
        
        try:
            # Make the request
            response: RecognizeResponse = self.stub.Recognize(
                request, 
                metadata=metadata,
                timeout=timeout
            )
            
            # Extract recognized text
            recognized_text = ""
            if response.results:
                recognized_text = " ".join([
                    result.alternatives[0].transcript 
                    for result in response.results 
                    if result.alternatives
                ])
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(recognized_text.encode()),
                duration_ms=duration_ms
            )
            
            # Log ASR-specific data
            self.logger.log_system_event("asr_recognition_success", 
                f"ASR recognition completed: {len(recognized_text)} characters", {
                    "request_id": request_id,
                    "input_file": audio_file_path,
                    "audio_duration_estimate": len(audio_data) / (sample_rate * 2),  # rough estimate
                    "text_length": len(recognized_text),
                    "language": language,
                    "processing_time_ms": duration_ms
                })
            
            return recognized_text
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            self.logger.log_request_error(
                request_id=request_id,
                error=e,
                duration_ms=duration_ms
            )
            
            raise
    
    def recognize_stream(self, audio_chunks: Iterator[bytes], language: str = "ru-RU",
                        model: Optional[str] = None, sample_rate: int = 16000,
                        timeout: float = 60.0) -> Iterator[str]:
        """
        Recognize speech from streaming audio with logging.
        
        Args:
            audio_chunks: Iterator of audio chunks
            language: Language code
            model: ASR model to use
            sample_rate: Audio sample rate
            timeout: Request timeout in seconds
            
        Yields:
            Partial recognition results
        """
        # Ensure connection
        self._ensure_connection()
        
        # Get auth metadata
        metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "language": language,
                "model": model or "default",
                "sample_rate": sample_rate,
                "service": "ASR_StreamRecognize",
                "streaming": True
            },
            auth_present=bool(metadata)
        )
        
        start_time = time.time()
        total_chunks = 0
        total_bytes = 0
        recognized_text_parts = []
        
        try:
            # Create streaming request generator
            def request_generator():
                # First request with config
                config_request = make_streaming_recognize_request(
                    audio_data=b"",  # Empty for config
                    language=language,
                    model=model,
                    sample_rate=sample_rate
                )
                yield config_request
                
                # Then stream audio chunks
                nonlocal total_chunks, total_bytes
                for chunk in audio_chunks:
                    total_chunks += 1
                    total_bytes += len(chunk)
                    audio_request = make_streaming_recognize_request(
                        audio_data=chunk,
                        language=language,
                        model=model,
                        sample_rate=sample_rate
                    )
                    yield audio_request
            
            # Make streaming request
            response_stream = self.stub.StreamingRecognize(
                request_generator(),
                metadata=metadata,
                timeout=timeout
            )
            
            for response in response_stream:
                if response.results:
                    for result in response.results:
                        if result.alternatives:
                            text = result.alternatives[0].transcript
                            recognized_text_parts.append(text)
                            yield text
            
            duration_ms = (time.time() - start_time) * 1000
            full_text = " ".join(recognized_text_parts)
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(full_text.encode()),
                duration_ms=duration_ms
            )
            
            # Log streaming-specific data
            self.logger.log_system_event("asr_stream_success", 
                f"ASR streaming completed: {total_chunks} chunks, {len(full_text)} characters", {
                    "request_id": request_id,
                    "total_chunks": total_chunks,
                    "total_bytes": total_bytes,
                    "text_length": len(full_text),
                    "language": language,
                    "processing_time_ms": duration_ms
                })
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            self.logger.log_request_error(
                request_id=request_id,
                error=e,
                duration_ms=duration_ms
            )
            
            raise
    
    def close(self):
        """Close the gRPC channel and log shutdown."""
        if self.channel:
            self.channel.close()
            self.logger.log_system_event("asr_client_shutdown", "ASR client closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def test_logged_asr(config_path: str, audio_file: str):
    """
    Test function for logged ASR recognition.
    
    Args:
        config_path: Path to configuration file
        audio_file: Path to audio file for testing
    """
    logger = get_logger()
    
    logger.log_system_event("asr_test_start", "Starting logged ASR recognition test", {
        "config_path": config_path,
        "audio_file": audio_file
    })
    
    try:
        with LoggedASRClient(config_path) as client:
            # Test file recognition
            text = client.recognize_file(
                audio_file_path=audio_file,
                language="ru-RU"
            )
            
            logger.log_system_event("asr_test_success", 
                f"ASR test completed successfully: '{text[:50]}...'", {
                    "recognized_text_length": len(text),
                    "audio_file": audio_file
                })
            
            return text
            
    except Exception as e:
        logger.log_system_event("asr_test_failed", f"ASR test failed: {e}", {
            "error": str(e),
            "error_type": type(e).__name__,
            "audio_file": audio_file
        })
        raise
