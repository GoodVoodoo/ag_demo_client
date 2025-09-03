"""
TTS Synthesis with professional logging integration.
Wraps the standard TTS synthesis with comprehensive request/response logging.
"""

import time
import grpc
from pathlib import Path
from typing import Optional, Iterator

from audiogram_client.common_utils.logging_config import get_logger
from audiogram_client.common_utils.config import Settings
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.connection import create_channel
from audiogram_client.tts.utils.request import make_tts_request
# from audiogram_client.tts.utils.definitions import TTSRequestInfo
from audiogram_client.genproto.tts_pb2_grpc import TTSStub
from audiogram_client.genproto.tts_pb2 import SynthesizeSpeechResponse
from audiogram_client.common_utils.types import TTSVoiceStyle


class LoggedTTSClient:
    """TTS client with comprehensive logging capabilities."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize logged TTS client.
        
        Args:
            config_path: Path to configuration file
        """
        self.logger = get_logger()
        self.settings = Settings([config_path] if config_path else [])
        self.channel = None
        self.stub = None
        
        # Log client initialization
        self.logger.log_system_event("client_init", "TTS client initialized", {
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
                self.stub = TTSStub(self.channel)
                
                # Test connection
                future = grpc.channel_ready_future(self.channel)
                future.result(timeout=10)
                
                duration = (time.time() - start_time) * 1000
                self.logger.log_system_event("connection_established", 
                    "gRPC channel established successfully", {
                        "endpoint": self.settings.api_address,
                        "duration_ms": duration
                    })
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                self.logger.log_system_event("connection_failed",
                    f"Failed to establish gRPC channel: {e}", {
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
            
            self.logger.log_auth_event("token_request", self.settings.sso_url, 
                                     True, f"Auth metadata obtained in {duration:.2f}ms")
            
            return metadata
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.logger.log_auth_event("token_request", self.settings.sso_url,
                                     False, f"Auth request failed after {duration:.2f}ms: {e}")
            raise
    
    def synthesize(self, text: str, voice_name: str = "gandzhaev", 
                  sample_rate: int = 22050, is_ssml: bool = False,
                  voice_style: TTSVoiceStyle = TTSVoiceStyle.neutral,
                  timeout: float = 30.0) -> bytes:
        """
        Synthesize speech with comprehensive logging.
        
        Args:
            text: Text to synthesize
            voice_name: Voice to use
            sample_rate: Audio sample rate
            is_ssml: Whether text is SSML
            voice_style: Voice style
            timeout: Request timeout in seconds
            
        Returns:
            Audio data as bytes
            
        Raises:
            Exception: If synthesis fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Create request
        request = make_tts_request(
            text=text,
            is_ssml=is_ssml,
            voice_name=voice_name,
            rate=sample_rate,
            voice_style=voice_style
        )
        
        # Get auth metadata
        metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data=request,
            auth_present=bool(metadata)
        )
        
        start_time = time.time()
        
        try:
            # Make the request
            response: SynthesizeSpeechResponse = self.stub.Synthesize(
                request, 
                metadata=metadata,
                timeout=timeout
            )
            
            # Get audio data
            audio_data = response.audio
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(audio_data),
                duration_ms=duration_ms
            )
            
            return audio_data
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            self.logger.log_request_error(
                request_id=request_id,
                error=e,
                duration_ms=duration_ms
            )
            
            raise
    
    def synthesize_stream(self, text: str, voice_name: str = "gandzhaev",
                         sample_rate: int = 22050, is_ssml: bool = False,
                         voice_style: TTSVoiceStyle = TTSVoiceStyle.neutral,
                         timeout: float = 30.0) -> Iterator[bytes]:
        """
        Synthesize speech with streaming response and logging.
        
        Args:
            text: Text to synthesize
            voice_name: Voice to use
            sample_rate: Audio sample rate
            is_ssml: Whether text is SSML
            voice_style: Voice style
            timeout: Request timeout in seconds
            
        Yields:
            Audio chunks as bytes
        """
        # Ensure connection
        self._ensure_connection()
        
        # Create request
        request = make_tts_request(
            text=text,
            is_ssml=is_ssml,
            voice_name=voice_name,
            rate=sample_rate,
            voice_style=voice_style
        )
        
        # Get auth metadata
        metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data=request,
            auth_present=bool(metadata)
        )
        
        start_time = time.time()
        total_bytes = 0
        
        try:
            # Make streaming request
            response_stream = self.stub.StreamSynthesize(
                request,
                metadata=metadata,
                timeout=timeout
            )
            
            for response in response_stream:
                chunk = response.audio
                total_bytes += len(chunk)
                yield chunk
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=total_bytes,
                duration_ms=duration_ms
            )
            
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
            self.logger.log_system_event("client_shutdown", "TTS client closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def test_logged_synthesis(config_path: str, output_file: str = "test_logged.wav"):
    """
    Test function for logged TTS synthesis.
    
    Args:
        config_path: Path to configuration file
        output_file: Output audio file path
    """
    logger = get_logger()
    
    logger.log_system_event("test_start", "Starting logged TTS synthesis test", {
        "config_path": config_path,
        "output_file": output_file
    })
    
    try:
        with LoggedTTSClient(config_path) as client:
            # Test synthesis
            audio_data = client.synthesize(
                text="Тестирование системы логирования AudioKit Dev SF",
                voice_name="gandzhaev",
                sample_rate=22050
            )
            
            # Save audio
            Path(output_file).write_bytes(audio_data)
            
            logger.log_system_event("test_success", 
                f"Test completed successfully, audio saved to {output_file}", {
                    "audio_size": len(audio_data),
                    "output_file": output_file
                })
            
            return True
            
    except Exception as e:
        logger.log_system_event("test_failed", f"Test failed: {e}", {
            "error": str(e),
            "error_type": type(e).__name__
        })
        return False
