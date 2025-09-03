"""
Universal Logged Client for all AudioKit operations.
Provides a single interface for TTS, ASR, Voice Cloning, Models, and Audio Archive
with comprehensive logging across all services.
"""

import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Union, Iterator

from audiogram_client.common_utils.logging_config import get_logger, init_logging
from audiogram_client.tts.logged_synthesize import LoggedTTSClient
from audiogram_client.asr.logged_recognize import LoggedASRClient
from audiogram_client.voice_cloning.logged_clone import LoggedVoiceCloningClient
from audiogram_client.models.logged_service import LoggedModelsClient
from audiogram_client.audio_archive.logged_archive import LoggedAudioArchiveClient
from audiogram_client.common_utils.types import TTSVoiceStyle


class UniversalAudioKitClient:
    """
    Universal client for all AudioKit operations with comprehensive logging.
    
    This client provides a unified interface for:
    - TTS (Text-to-Speech) synthesis
    - ASR (Automatic Speech Recognition)
    - Voice Cloning operations
    - Models service queries
    - Audio Archive management
    
    All operations are logged with request correlation, timing, and error tracking.
    """
    
    def __init__(self, config_path: Optional[str] = None, log_dir: str = "logs", 
                 log_level: str = "INFO"):
        """
        Initialize the universal AudioKit client with logging.
        
        Args:
            config_path: Path to configuration file
            log_dir: Directory for log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        # Initialize logging system
        self.logger = init_logging(log_dir=log_dir, log_level=log_level)
        
        # Store configuration
        self.config_path = config_path
        
        # Initialize service clients (lazy loading)
        self._tts_client = None
        self._asr_client = None
        self._voice_cloning_client = None
        self._models_client = None
        self._audio_archive_client = None
        
        # Log universal client initialization
        self.logger.log_system_event("universal_client_init", 
            "Universal AudioKit client initialized", {
                "config_path": config_path,
                "log_dir": log_dir,
                "log_level": log_level,
                "services": ["TTS", "ASR", "VoiceCloning", "Models", "AudioArchive"]
            })
    
    # TTS Operations
    @property
    def tts(self) -> LoggedTTSClient:
        """Get TTS client with lazy initialization."""
        if self._tts_client is None:
            self._tts_client = LoggedTTSClient(self.config_path)
        return self._tts_client
    
    def synthesize_text(self, text: str, voice_name: str = "gandzhaev", 
                       sample_rate: int = 22050, is_ssml: bool = False,
                       voice_style: TTSVoiceStyle = TTSVoiceStyle.neutral,
                       save_to: Optional[str] = None) -> bytes:
        """
        Synthesize speech from text with comprehensive logging.
        
        Args:
            text: Text to synthesize
            voice_name: Voice to use
            sample_rate: Audio sample rate
            is_ssml: Whether text is SSML
            voice_style: Voice style
            save_to: Optional file path to save audio
            
        Returns:
            Audio data as bytes
        """
        start_time = time.time()
        
        try:
            audio_data = self.tts.synthesize(
                text=text,
                voice_name=voice_name,
                sample_rate=sample_rate,
                is_ssml=is_ssml,
                voice_style=voice_style
            )
            
            # Save to file if requested
            if save_to:
                Path(save_to).write_bytes(audio_data)
                self.logger.log_system_event("tts_file_saved", 
                    f"TTS audio saved to {save_to}", {
                        "output_file": save_to,
                        "audio_size_bytes": len(audio_data),
                        "text_length": len(text)
                    })
            
            return audio_data
            
        except Exception as e:
            self.logger.log_system_event("tts_operation_failed", 
                f"TTS synthesis failed: {e}", {
                    "error": str(e),
                    "text_length": len(text),
                    "voice_name": voice_name
                })
            raise
    
    # ASR Operations
    @property
    def asr(self) -> LoggedASRClient:
        """Get ASR client with lazy initialization."""
        if self._asr_client is None:
            self._asr_client = LoggedASRClient(self.config_path)
        return self._asr_client
    
    def recognize_audio(self, audio_file_path: str, language: str = "ru-RU",
                       model: Optional[str] = None, sample_rate: int = 16000,
                       save_transcript_to: Optional[str] = None) -> str:
        """
        Recognize speech from audio file with comprehensive logging.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code
            model: ASR model to use
            sample_rate: Audio sample rate
            save_transcript_to: Optional file path to save transcript
            
        Returns:
            Recognized text
        """
        try:
            text = self.asr.recognize_file(
                audio_file_path=audio_file_path,
                language=language,
                model=model,
                sample_rate=sample_rate
            )
            
            # Save transcript if requested
            if save_transcript_to:
                Path(save_transcript_to).write_text(text, encoding='utf-8')
                self.logger.log_system_event("asr_transcript_saved", 
                    f"ASR transcript saved to {save_transcript_to}", {
                        "output_file": save_transcript_to,
                        "transcript_length": len(text),
                        "audio_file": audio_file_path
                    })
            
            return text
            
        except Exception as e:
            self.logger.log_system_event("asr_operation_failed", 
                f"ASR recognition failed: {e}", {
                    "error": str(e),
                    "audio_file": audio_file_path,
                    "language": language
                })
            raise
    
    # Voice Cloning Operations
    @property
    def voice_cloning(self) -> LoggedVoiceCloningClient:
        """Get Voice Cloning client with lazy initialization."""
        if self._voice_cloning_client is None:
            self._voice_cloning_client = LoggedVoiceCloningClient(self.config_path)
        return self._voice_cloning_client
    
    def clone_voice(self, voice_name: str, audio_files: List[str], 
                   description: str = "") -> str:
        """
        Clone a voice with comprehensive logging.
        
        Args:
            voice_name: Name for the cloned voice
            audio_files: List of audio file paths for training
            description: Description of the voice
            
        Returns:
            Task ID for the cloning operation
        """
        return self.voice_cloning.clone_voice(
            voice_name=voice_name,
            audio_files=audio_files,
            description=description
        )
    
    def delete_voice(self, voice_name: str) -> bool:
        """Delete a cloned voice with logging."""
        return self.voice_cloning.delete_voice(voice_name)
    
    def get_voice_task_info(self, task_id: str) -> Dict[str, Any]:
        """Get voice cloning task information with logging."""
        return self.voice_cloning.get_task_info(task_id)
    
    # Models Operations
    @property
    def models(self) -> LoggedModelsClient:
        """Get Models client with lazy initialization."""
        if self._models_client is None:
            self._models_client = LoggedModelsClient(self.config_path)
        return self._models_client
    
    def get_available_models(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all available models with comprehensive logging."""
        return self.models.get_all_models()
    
    def get_tts_models(self) -> List[Dict[str, Any]]:
        """Get available TTS models with logging."""
        return self.models.get_tts_models()
    
    def get_asr_models(self) -> List[Dict[str, Any]]:
        """Get available ASR models with logging."""
        return self.models.get_asr_models()
    
    # Audio Archive Operations
    @property
    def audio_archive(self) -> LoggedAudioArchiveClient:
        """Get Audio Archive client with lazy initialization."""
        if self._audio_archive_client is None:
            self._audio_archive_client = LoggedAudioArchiveClient(self.config_path)
        return self._audio_archive_client
    
    def archive_audio(self, audio_data: bytes, filename: str, 
                     metadata: Dict[str, Any] = None) -> str:
        """Save audio to archive with logging."""
        return self.audio_archive.save_audio(
            audio_data=audio_data,
            filename=filename,
            metadata=metadata
        )
    
    def archive_transcript(self, transcript: str, audio_id: str, 
                          language: str = "ru-RU") -> str:
        """Save transcript to archive with logging."""
        return self.audio_archive.save_transcript(
            transcript=transcript,
            audio_id=audio_id,
            language=language
        )
    
    # Workflow Operations
    def text_to_speech_workflow(self, text: str, voice_name: str = "gandzhaev",
                               output_file: Optional[str] = None,
                               archive_audio: bool = False) -> Dict[str, Any]:
        """
        Complete TTS workflow with optional archiving.
        
        Args:
            text: Text to synthesize
            voice_name: Voice to use
            output_file: Optional output file path
            archive_audio: Whether to archive the audio
            
        Returns:
            Workflow results
        """
        workflow_id = f"tts_workflow_{int(time.time())}"
        start_time = time.time()
        
        self.logger.log_system_event("workflow_start", 
            f"Starting TTS workflow: {workflow_id}", {
                "workflow_id": workflow_id,
                "text_length": len(text),
                "voice_name": voice_name,
                "archive_audio": archive_audio
            })
        
        try:
            # Synthesize audio
            audio_data = self.synthesize_text(
                text=text,
                voice_name=voice_name,
                save_to=output_file
            )
            
            results = {
                "workflow_id": workflow_id,
                "audio_size_bytes": len(audio_data),
                "output_file": output_file,
                "archive_id": None
            }
            
            # Archive if requested
            if archive_audio:
                filename = output_file or f"{workflow_id}.wav"
                archive_id = self.archive_audio(
                    audio_data=audio_data,
                    filename=filename,
                    metadata={
                        "workflow_id": workflow_id,
                        "text": text,
                        "voice_name": voice_name
                    }
                )
                results["archive_id"] = archive_id
            
            duration_ms = (time.time() - start_time) * 1000
            
            self.logger.log_system_event("workflow_success", 
                f"TTS workflow completed: {workflow_id}", {
                    "workflow_id": workflow_id,
                    "duration_ms": duration_ms,
                    "results": results
                })
            
            return results
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            self.logger.log_system_event("workflow_failed", 
                f"TTS workflow failed: {workflow_id} - {e}", {
                    "workflow_id": workflow_id,
                    "duration_ms": duration_ms,
                    "error": str(e)
                })
            raise
    
    def speech_to_text_workflow(self, audio_file: str, language: str = "ru-RU",
                               output_file: Optional[str] = None,
                               archive_transcript: bool = False) -> Dict[str, Any]:
        """
        Complete ASR workflow with optional archiving.
        
        Args:
            audio_file: Input audio file path
            language: Language code
            output_file: Optional transcript output file
            archive_transcript: Whether to archive the transcript
            
        Returns:
            Workflow results
        """
        workflow_id = f"asr_workflow_{int(time.time())}"
        start_time = time.time()
        
        self.logger.log_system_event("workflow_start", 
            f"Starting ASR workflow: {workflow_id}", {
                "workflow_id": workflow_id,
                "audio_file": audio_file,
                "language": language,
                "archive_transcript": archive_transcript
            })
        
        try:
            # Recognize speech
            transcript = self.recognize_audio(
                audio_file_path=audio_file,
                language=language,
                save_transcript_to=output_file
            )
            
            results = {
                "workflow_id": workflow_id,
                "transcript": transcript,
                "transcript_length": len(transcript),
                "output_file": output_file,
                "archive_id": None
            }
            
            # Archive if requested
            if archive_transcript:
                # First archive the audio
                audio_data = Path(audio_file).read_bytes()
                audio_archive_id = self.archive_audio(
                    audio_data=audio_data,
                    filename=Path(audio_file).name,
                    metadata={
                        "workflow_id": workflow_id,
                        "language": language
                    }
                )
                
                # Then archive the transcript
                transcript_archive_id = self.archive_transcript(
                    transcript=transcript,
                    audio_id=audio_archive_id,
                    language=language
                )
                results["archive_id"] = transcript_archive_id
            
            duration_ms = (time.time() - start_time) * 1000
            
            self.logger.log_system_event("workflow_success", 
                f"ASR workflow completed: {workflow_id}", {
                    "workflow_id": workflow_id,
                    "duration_ms": duration_ms,
                    "results": results
                })
            
            return results
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            self.logger.log_system_event("workflow_failed", 
                f"ASR workflow failed: {workflow_id} - {e}", {
                    "workflow_id": workflow_id,
                    "duration_ms": duration_ms,
                    "error": str(e)
                })
            raise
    
    # Health and Status
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on all services.
        
        Returns:
            Health status of all services
        """
        health_status = {
            "timestamp": time.time(),
            "services": {},
            "overall_status": "healthy"
        }
        
        self.logger.log_system_event("health_check_start", "Starting comprehensive health check")
        
        # Check each service
        services = {
            "tts": self.tts,
            "asr": self.asr,
            "voice_cloning": self.voice_cloning,
            "models": self.models,
            "audio_archive": self.audio_archive
        }
        
        for service_name, service_client in services.items():
            try:
                start_time = time.time()
                service_client._ensure_connection()
                duration_ms = (time.time() - start_time) * 1000
                
                health_status["services"][service_name] = {
                    "status": "healthy",
                    "response_time_ms": duration_ms
                }
                
            except Exception as e:
                health_status["services"][service_name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                health_status["overall_status"] = "degraded"
        
        self.logger.log_system_event("health_check_complete", 
            f"Health check completed: {health_status['overall_status']}", {
                "health_status": health_status
            })
        
        return health_status
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get logging statistics and system information."""
        return self.logger.get_log_stats()
    
    def close(self):
        """Close all service clients and log shutdown."""
        clients = [
            self._tts_client,
            self._asr_client,
            self._voice_cloning_client,
            self._models_client,
            self._audio_archive_client
        ]
        
        for client in clients:
            if client:
                try:
                    client.close()
                except Exception:
                    pass
        
        self.logger.log_system_event("universal_client_shutdown", 
            "Universal AudioKit client closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Convenience function
def create_audiokit_client(config_path: str = "config_audiokit_dev_sf.ini",
                          log_dir: str = "logs", 
                          log_level: str = "INFO") -> UniversalAudioKitClient:
    """
    Create a universal AudioKit client with logging.
    
    Args:
        config_path: Path to configuration file
        log_dir: Directory for log files
        log_level: Logging level
        
    Returns:
        Configured universal client
    """
    return UniversalAudioKitClient(
        config_path=config_path,
        log_dir=log_dir,
        log_level=log_level
    )
