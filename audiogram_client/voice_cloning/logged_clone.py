"""
Voice Cloning with professional logging integration.
Wraps voice cloning operations with comprehensive request/response logging.
"""

import time
import grpc
from pathlib import Path
from typing import Optional, Dict, Any

from audiogram_client.common_utils.logging_config import get_logger
from audiogram_client.common_utils.config import Settings
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.connection import create_channel
from audiogram_client.voice_cloning.utils.arguments import CloneVoiceArgs, DeleteVoiceArgs, GetTaskInfoArgs
from audiogram_client.genproto.voice_cloning_pb2_grpc import VoiceCloningStub
from audiogram_client.genproto.voice_cloning_pb2 import CloneVoiceResponse, DeleteVoiceResponse, GetTaskInfoResponse


class LoggedVoiceCloningClient:
    """Voice Cloning client with comprehensive logging capabilities."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize logged Voice Cloning client.
        
        Args:
            config_path: Path to configuration file
        """
        self.logger = get_logger()
        self.settings = Settings([config_path] if config_path else [])
        self.channel = None
        self.stub = None
        
        # Log client initialization
        self.logger.log_system_event("voice_cloning_client_init", "Voice Cloning client initialized", {
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
                self.stub = VoiceCloningStub(self.channel)
                
                # Test connection
                future = grpc.channel_ready_future(self.channel)
                future.result(timeout=10)
                
                duration = (time.time() - start_time) * 1000
                self.logger.log_system_event("voice_cloning_connection_established", 
                    "Voice Cloning gRPC channel established successfully", {
                        "endpoint": self.settings.api_address,
                        "duration_ms": duration
                    })
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                self.logger.log_system_event("voice_cloning_connection_failed",
                    f"Failed to establish Voice Cloning gRPC channel: {e}", {
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
            
            self.logger.log_auth_event("voice_cloning_token_request", self.settings.sso_url, 
                                     True, f"Voice Cloning auth metadata obtained in {duration:.2f}ms")
            
            return metadata
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.logger.log_auth_event("voice_cloning_token_request", self.settings.sso_url,
                                     False, f"Voice Cloning auth request failed after {duration:.2f}ms: {e}")
            raise
    
    def clone_voice(self, voice_name: str, audio_files: list, description: str = "",
                   timeout: float = 300.0) -> str:
        """
        Clone a voice with comprehensive logging.
        
        Args:
            voice_name: Name for the cloned voice
            audio_files: List of audio file paths for training
            description: Description of the voice
            timeout: Request timeout in seconds
            
        Returns:
            Task ID for the cloning operation
            
        Raises:
            Exception: If voice cloning fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Prepare audio data
        audio_data = []
        total_audio_size = 0
        
        for audio_file in audio_files:
            audio_path = Path(audio_file)
            if not audio_path.exists():
                raise FileNotFoundError(f"Audio file not found: {audio_file}")
            
            data = audio_path.read_bytes()
            audio_data.append(data)
            total_audio_size += len(data)
        
        # Create request
        args = CloneVoiceArgs(
            voice_name=voice_name,
            audio_files=audio_files,
            description=description
        )
        
        # Get auth metadata
        metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "voice_name": voice_name,
                "description": description,
                "audio_files": audio_files,
                "audio_files_count": len(audio_files),
                "total_audio_size_bytes": total_audio_size,
                "service": "VoiceCloning_Clone"
            },
            auth_present=bool(metadata)
        )
        
        start_time = time.time()
        
        try:
            # Make the request (using the actual implementation)
            from audiogram_client.voice_cloning.clone_voice import clone_voice_impl
            
            response = clone_voice_impl(
                args=args,
                settings=self.settings,
                stub=self.stub,
                metadata=metadata
            )
            
            # Extract task ID
            task_id = response.task_id if hasattr(response, 'task_id') else str(response)
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(task_id.encode()),
                duration_ms=duration_ms
            )
            
            # Log voice cloning specific data
            self.logger.log_system_event("voice_cloning_success", 
                f"Voice cloning started: '{voice_name}' -> {task_id}", {
                    "request_id": request_id,
                    "voice_name": voice_name,
                    "task_id": task_id,
                    "audio_files_count": len(audio_files),
                    "total_audio_mb": total_audio_size / (1024 * 1024),
                    "processing_time_ms": duration_ms
                })
            
            return task_id
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            self.logger.log_request_error(
                request_id=request_id,
                error=e,
                duration_ms=duration_ms
            )
            
            raise
    
    def delete_voice(self, voice_name: str, timeout: float = 30.0) -> bool:
        """
        Delete a cloned voice with logging.
        
        Args:
            voice_name: Name of the voice to delete
            timeout: Request timeout in seconds
            
        Returns:
            True if deletion was successful
            
        Raises:
            Exception: If voice deletion fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Create request
        args = DeleteVoiceArgs(voice_name=voice_name)
        
        # Get auth metadata
        metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "voice_name": voice_name,
                "service": "VoiceCloning_Delete"
            },
            auth_present=bool(metadata)
        )
        
        start_time = time.time()
        
        try:
            # Make the request
            from audiogram_client.voice_cloning.delete_voice import delete_voice_impl
            
            response = delete_voice_impl(
                args=args,
                settings=self.settings,
                stub=self.stub,
                metadata=metadata
            )
            
            success = response.success if hasattr(response, 'success') else True
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=1,  # Boolean response
                duration_ms=duration_ms
            )
            
            # Log deletion specific data
            self.logger.log_system_event("voice_deletion_success", 
                f"Voice deleted: '{voice_name}'", {
                    "request_id": request_id,
                    "voice_name": voice_name,
                    "success": success,
                    "processing_time_ms": duration_ms
                })
            
            return success
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            self.logger.log_request_error(
                request_id=request_id,
                error=e,
                duration_ms=duration_ms
            )
            
            raise
    
    def get_task_info(self, task_id: str, timeout: float = 30.0) -> Dict[str, Any]:
        """
        Get voice cloning task information with logging.
        
        Args:
            task_id: Task ID to query
            timeout: Request timeout in seconds
            
        Returns:
            Task information dictionary
            
        Raises:
            Exception: If task info retrieval fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Create request
        args = GetTaskInfoArgs(task_id=task_id)
        
        # Get auth metadata
        metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "task_id": task_id,
                "service": "VoiceCloning_GetTaskInfo"
            },
            auth_present=bool(metadata)
        )
        
        start_time = time.time()
        
        try:
            # Make the request
            from audiogram_client.voice_cloning.get_task_info import get_task_info_impl
            
            response = get_task_info_impl(
                args=args,
                settings=self.settings,
                stub=self.stub,
                metadata=metadata
            )
            
            # Convert response to dict
            task_info = {
                "task_id": task_id,
                "status": getattr(response, 'status', 'unknown'),
                "progress": getattr(response, 'progress', 0),
                "message": getattr(response, 'message', ''),
                "created_at": getattr(response, 'created_at', ''),
                "updated_at": getattr(response, 'updated_at', '')
            }
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(str(task_info).encode()),
                duration_ms=duration_ms
            )
            
            # Log task info specific data
            self.logger.log_system_event("voice_task_info_success", 
                f"Task info retrieved: {task_id} -> {task_info.get('status', 'unknown')}", {
                    "request_id": request_id,
                    "task_id": task_id,
                    "task_status": task_info.get('status'),
                    "task_progress": task_info.get('progress'),
                    "processing_time_ms": duration_ms
                })
            
            return task_info
            
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
            self.logger.log_system_event("voice_cloning_client_shutdown", "Voice Cloning client closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def test_logged_voice_cloning(config_path: str, voice_name: str, audio_files: list):
    """
    Test function for logged voice cloning operations.
    
    Args:
        config_path: Path to configuration file
        voice_name: Name for the test voice
        audio_files: List of audio files for training
    """
    logger = get_logger()
    
    logger.log_system_event("voice_cloning_test_start", "Starting logged voice cloning test", {
        "config_path": config_path,
        "voice_name": voice_name,
        "audio_files": audio_files
    })
    
    try:
        with LoggedVoiceCloningClient(config_path) as client:
            # Test voice cloning
            task_id = client.clone_voice(
                voice_name=voice_name,
                audio_files=audio_files,
                description=f"Test voice cloning for {voice_name}"
            )
            
            # Test task info
            task_info = client.get_task_info(task_id)
            
            logger.log_system_event("voice_cloning_test_success", 
                f"Voice cloning test completed: {task_id}", {
                    "voice_name": voice_name,
                    "task_id": task_id,
                    "task_status": task_info.get('status')
                })
            
            return task_id, task_info
            
    except Exception as e:
        logger.log_system_event("voice_cloning_test_failed", f"Voice cloning test failed: {e}", {
            "error": str(e),
            "error_type": type(e).__name__,
            "voice_name": voice_name
        })
        raise
