"""
Audio Archive with professional logging integration.
Wraps audio archive operations with comprehensive request/response logging.
"""

import time
import grpc
from pathlib import Path
from typing import Optional, Dict, Any, List

from audiogram_client.common_utils.logging_config import get_logger
from audiogram_client.common_utils.config import Settings
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.connection import create_channel


class LoggedAudioArchiveClient:
    """Audio Archive client with comprehensive logging capabilities."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize logged Audio Archive client.
        
        Args:
            config_path: Path to configuration file
        """
        self.logger = get_logger()
        self.settings = Settings([config_path] if config_path else [])
        self.channel = None
        
        # Log client initialization
        self.logger.log_system_event("audio_archive_client_init", "Audio Archive client initialized", {
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
                
                # Test connection
                future = grpc.channel_ready_future(self.channel)
                future.result(timeout=10)
                
                duration = (time.time() - start_time) * 1000
                self.logger.log_system_event("audio_archive_connection_established", 
                    "Audio Archive gRPC channel established successfully", {
                        "endpoint": self.settings.api_address,
                        "duration_ms": duration
                    })
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                self.logger.log_system_event("audio_archive_connection_failed",
                    f"Failed to establish Audio Archive gRPC channel: {e}", {
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
            
            self.logger.log_auth_event("audio_archive_token_request", self.settings.sso_url, 
                                     True, f"Audio Archive auth metadata obtained in {duration:.2f}ms")
            
            return metadata
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.logger.log_auth_event("audio_archive_token_request", self.settings.sso_url,
                                     False, f"Audio Archive auth request failed after {duration:.2f}ms: {e}")
            raise
    
    def save_audio(self, audio_data: bytes, filename: str, metadata: Dict[str, Any] = None,
                  timeout: float = 60.0) -> str:
        """
        Save audio to archive with comprehensive logging.
        
        Args:
            audio_data: Raw audio data
            filename: Name for the archived file
            metadata: Additional metadata for the audio
            timeout: Request timeout in seconds
            
        Returns:
            Archive ID or path
            
        Raises:
            Exception: If audio saving fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Get auth metadata
        auth_metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "filename": filename,
                "audio_size_bytes": len(audio_data),
                "metadata": metadata or {},
                "service": "AudioArchive_SaveAudio"
            },
            auth_present=bool(auth_metadata)
        )
        
        start_time = time.time()
        
        try:
            # Make the request using existing implementation
            from audiogram_client.audio_archive.save_audio import save_audio_impl
            
            # Create arguments object (mock structure)
            class SaveAudioArgs:
                def __init__(self, filename, audio_data, metadata):
                    self.filename = filename
                    self.audio_data = audio_data
                    self.metadata = metadata or {}
            
            args = SaveAudioArgs(filename, audio_data, metadata)
            
            # Call implementation
            result = save_audio_impl(args, self.settings, auth_metadata)
            archive_id = str(result) if result else filename
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(archive_id.encode()),
                duration_ms=duration_ms
            )
            
            # Log audio archive specific data
            self.logger.log_system_event("audio_save_success", 
                f"Audio saved to archive: '{filename}' -> {archive_id}", {
                    "request_id": request_id,
                    "filename": filename,
                    "archive_id": archive_id,
                    "audio_size_mb": len(audio_data) / (1024 * 1024),
                    "metadata_keys": list((metadata or {}).keys()),
                    "processing_time_ms": duration_ms
                })
            
            return archive_id
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            self.logger.log_request_error(
                request_id=request_id,
                error=e,
                duration_ms=duration_ms
            )
            
            raise
    
    def save_transcript(self, transcript: str, audio_id: str, language: str = "ru-RU",
                       confidence_scores: List[float] = None, timeout: float = 30.0) -> str:
        """
        Save transcript to archive with comprehensive logging.
        
        Args:
            transcript: Recognized text
            audio_id: Associated audio ID
            language: Language of the transcript
            confidence_scores: Confidence scores for recognition
            timeout: Request timeout in seconds
            
        Returns:
            Transcript ID
            
        Raises:
            Exception: If transcript saving fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Get auth metadata
        auth_metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "audio_id": audio_id,
                "transcript_length": len(transcript),
                "language": language,
                "confidence_scores_count": len(confidence_scores or []),
                "service": "AudioArchive_SaveTranscript"
            },
            auth_present=bool(auth_metadata)
        )
        
        start_time = time.time()
        
        try:
            # Make the request using existing implementation
            from audiogram_client.audio_archive.save_transcript import save_transcript_impl
            
            # Create arguments object (mock structure)
            class SaveTranscriptArgs:
                def __init__(self, transcript, audio_id, language, confidence_scores):
                    self.transcript = transcript
                    self.audio_id = audio_id
                    self.language = language
                    self.confidence_scores = confidence_scores or []
            
            args = SaveTranscriptArgs(transcript, audio_id, language, confidence_scores)
            
            # Call implementation
            result = save_transcript_impl(args, self.settings, auth_metadata)
            transcript_id = str(result) if result else f"{audio_id}_transcript"
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(transcript.encode()),
                duration_ms=duration_ms
            )
            
            # Log transcript specific data
            self.logger.log_system_event("transcript_save_success", 
                f"Transcript saved: {len(transcript)} chars -> {transcript_id}", {
                    "request_id": request_id,
                    "audio_id": audio_id,
                    "transcript_id": transcript_id,
                    "transcript_length": len(transcript),
                    "language": language,
                    "confidence_scores_count": len(confidence_scores or []),
                    "avg_confidence": sum(confidence_scores or [0]) / max(len(confidence_scores or []), 1),
                    "processing_time_ms": duration_ms
                })
            
            return transcript_id
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            self.logger.log_request_error(
                request_id=request_id,
                error=e,
                duration_ms=duration_ms
            )
            
            raise
    
    def save_vad_marks(self, vad_marks: List[Dict[str, float]], audio_id: str,
                      timeout: float = 30.0) -> str:
        """
        Save VAD (Voice Activity Detection) marks with comprehensive logging.
        
        Args:
            vad_marks: List of VAD segments with start/end times
            audio_id: Associated audio ID
            timeout: Request timeout in seconds
            
        Returns:
            VAD marks ID
            
        Raises:
            Exception: If VAD marks saving fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Get auth metadata
        auth_metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "audio_id": audio_id,
                "vad_segments_count": len(vad_marks),
                "total_speech_duration": sum(
                    mark.get('end', 0) - mark.get('start', 0) 
                    for mark in vad_marks
                ),
                "service": "AudioArchive_SaveVADMarks"
            },
            auth_present=bool(auth_metadata)
        )
        
        start_time = time.time()
        
        try:
            # Make the request using existing implementation
            from audiogram_client.audio_archive.save_vad_marks import save_vad_marks_impl
            
            # Create arguments object (mock structure)
            class SaveVADMarksArgs:
                def __init__(self, vad_marks, audio_id):
                    self.vad_marks = vad_marks
                    self.audio_id = audio_id
            
            args = SaveVADMarksArgs(vad_marks, audio_id)
            
            # Call implementation
            result = save_vad_marks_impl(args, self.settings, auth_metadata)
            vad_id = str(result) if result else f"{audio_id}_vad"
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(str(vad_marks).encode()),
                duration_ms=duration_ms
            )
            
            # Calculate VAD statistics
            total_duration = sum(mark.get('end', 0) - mark.get('start', 0) for mark in vad_marks)
            
            # Log VAD specific data
            self.logger.log_system_event("vad_marks_save_success", 
                f"VAD marks saved: {len(vad_marks)} segments -> {vad_id}", {
                    "request_id": request_id,
                    "audio_id": audio_id,
                    "vad_id": vad_id,
                    "segments_count": len(vad_marks),
                    "total_speech_duration_seconds": total_duration,
                    "avg_segment_duration": total_duration / max(len(vad_marks), 1),
                    "processing_time_ms": duration_ms
                })
            
            return vad_id
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            self.logger.log_request_error(
                request_id=request_id,
                error=e,
                duration_ms=duration_ms
            )
            
            raise
    
    def get_archive_requests(self, limit: int = 100, offset: int = 0,
                           timeout: float = 30.0) -> List[Dict[str, Any]]:
        """
        Get archive requests with comprehensive logging.
        
        Args:
            limit: Maximum number of requests to retrieve
            offset: Offset for pagination
            timeout: Request timeout in seconds
            
        Returns:
            List of archive requests
            
        Raises:
            Exception: If archive requests retrieval fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Get auth metadata
        auth_metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "limit": limit,
                "offset": offset,
                "service": "AudioArchive_GetRequests"
            },
            auth_present=bool(auth_metadata)
        )
        
        start_time = time.time()
        
        try:
            # Make the request using existing implementation
            from audiogram_client.audio_archive.get_requests import get_requests_impl
            
            # Create arguments object (mock structure)
            class GetRequestsArgs:
                def __init__(self, limit, offset):
                    self.limit = limit
                    self.offset = offset
            
            args = GetRequestsArgs(limit, offset)
            
            # Call implementation
            requests = get_requests_impl(args, self.settings, auth_metadata)
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(str(requests).encode()),
                duration_ms=duration_ms
            )
            
            # Log requests specific data
            self.logger.log_system_event("archive_requests_success", 
                f"Archive requests retrieved: {len(requests)} items", {
                    "request_id": request_id,
                    "requests_count": len(requests),
                    "limit": limit,
                    "offset": offset,
                    "processing_time_ms": duration_ms
                })
            
            return requests
            
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
            self.logger.log_system_event("audio_archive_client_shutdown", "Audio Archive client closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def test_logged_audio_archive(config_path: str, test_audio_file: str):
    """
    Test function for logged audio archive operations.
    
    Args:
        config_path: Path to configuration file
        test_audio_file: Path to test audio file
    """
    logger = get_logger()
    
    logger.log_system_event("audio_archive_test_start", "Starting logged audio archive test", {
        "config_path": config_path,
        "test_audio_file": test_audio_file
    })
    
    try:
        with LoggedAudioArchiveClient(config_path) as client:
            # Read test audio
            audio_path = Path(test_audio_file)
            if not audio_path.exists():
                raise FileNotFoundError(f"Test audio file not found: {test_audio_file}")
            
            audio_data = audio_path.read_bytes()
            
            # Test audio saving
            archive_id = client.save_audio(
                audio_data=audio_data,
                filename=audio_path.name,
                metadata={"test": True, "source": "logging_test"}
            )
            
            # Test transcript saving
            transcript_id = client.save_transcript(
                transcript="Тестовый текст для архива",
                audio_id=archive_id,
                language="ru-RU",
                confidence_scores=[0.95, 0.87, 0.92]
            )
            
            # Test VAD marks saving
            vad_id = client.save_vad_marks(
                vad_marks=[
                    {"start": 0.0, "end": 2.5},
                    {"start": 3.0, "end": 5.5},
                    {"start": 6.0, "end": 8.0}
                ],
                audio_id=archive_id
            )
            
            logger.log_system_event("audio_archive_test_success", 
                "Audio archive test completed successfully", {
                    "archive_id": archive_id,
                    "transcript_id": transcript_id,
                    "vad_id": vad_id,
                    "test_audio_file": test_audio_file
                })
            
            return {
                "archive_id": archive_id,
                "transcript_id": transcript_id,
                "vad_id": vad_id
            }
            
    except Exception as e:
        logger.log_system_event("audio_archive_test_failed", f"Audio archive test failed: {e}", {
            "error": str(e),
            "error_type": type(e).__name__,
            "test_audio_file": test_audio_file
        })
        raise
