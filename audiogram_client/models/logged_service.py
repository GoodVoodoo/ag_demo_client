"""
Models Service with professional logging integration.
Wraps model queries with comprehensive request/response logging.
"""

import time
import grpc
from typing import Optional, Dict, Any, List

from audiogram_client.common_utils.logging_config import get_logger
from audiogram_client.common_utils.config import Settings
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.connection import create_channel


class LoggedModelsClient:
    """Models service client with comprehensive logging capabilities."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize logged Models client.
        
        Args:
            config_path: Path to configuration file
        """
        self.logger = get_logger()
        self.settings = Settings([config_path] if config_path else [])
        self.channel = None
        
        # Log client initialization
        self.logger.log_system_event("models_client_init", "Models service client initialized", {
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
                self.logger.log_system_event("models_connection_established", 
                    "Models service gRPC channel established successfully", {
                        "endpoint": self.settings.api_address,
                        "duration_ms": duration
                    })
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                self.logger.log_system_event("models_connection_failed",
                    f"Failed to establish Models service gRPC channel: {e}", {
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
            
            self.logger.log_auth_event("models_token_request", self.settings.sso_url, 
                                     True, f"Models service auth metadata obtained in {duration:.2f}ms")
            
            return metadata
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.logger.log_auth_event("models_token_request", self.settings.sso_url,
                                     False, f"Models service auth request failed after {duration:.2f}ms: {e}")
            raise
    
    def get_tts_models(self, timeout: float = 30.0) -> List[Dict[str, Any]]:
        """
        Get available TTS models with comprehensive logging.
        
        Args:
            timeout: Request timeout in seconds
            
        Returns:
            List of TTS model information
            
        Raises:
            Exception: If model query fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Get auth metadata
        metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "service": "Models_GetTTSModels",
                "query_type": "tts_models"
            },
            auth_present=bool(metadata)
        )
        
        start_time = time.time()
        
        try:
            # Make the request using the existing implementation
            from audiogram_client.tts.get_models_info import get_tts_models_info
            
            models = get_tts_models_info(self.settings)
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(str(models).encode()),
                duration_ms=duration_ms
            )
            
            # Log models specific data
            self.logger.log_system_event("tts_models_query_success", 
                f"TTS models retrieved: {len(models)} models", {
                    "request_id": request_id,
                    "models_count": len(models),
                    "model_names": [model.get('name', 'unknown') for model in models] if isinstance(models, list) else [],
                    "processing_time_ms": duration_ms
                })
            
            return models
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            self.logger.log_request_error(
                request_id=request_id,
                error=e,
                duration_ms=duration_ms
            )
            
            raise
    
    def get_asr_models(self, timeout: float = 30.0) -> List[Dict[str, Any]]:
        """
        Get available ASR models with comprehensive logging.
        
        Args:
            timeout: Request timeout in seconds
            
        Returns:
            List of ASR model information
            
        Raises:
            Exception: If model query fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Get auth metadata
        metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "service": "Models_GetASRModels",
                "query_type": "asr_models"
            },
            auth_present=bool(metadata)
        )
        
        start_time = time.time()
        
        try:
            # Make the request using the existing implementation
            from audiogram_client.asr.get_models_info import get_asr_models_info
            
            models = get_asr_models_info(self.settings)
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(str(models).encode()),
                duration_ms=duration_ms
            )
            
            # Log models specific data
            self.logger.log_system_event("asr_models_query_success", 
                f"ASR models retrieved: {len(models)} models", {
                    "request_id": request_id,
                    "models_count": len(models),
                    "model_names": [model.get('name', 'unknown') for model in models] if isinstance(models, list) else [],
                    "processing_time_ms": duration_ms
                })
            
            return models
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            self.logger.log_request_error(
                request_id=request_id,
                error=e,
                duration_ms=duration_ms
            )
            
            raise
    
    def get_voice_cloning_models(self, timeout: float = 30.0) -> List[Dict[str, Any]]:
        """
        Get available voice cloning models with comprehensive logging.
        
        Args:
            timeout: Request timeout in seconds
            
        Returns:
            List of voice cloning model information
            
        Raises:
            Exception: If model query fails
        """
        # Ensure connection
        self._ensure_connection()
        
        # Get auth metadata
        metadata = self._get_auth_metadata()
        
        # Start logging
        request_id = self.logger.log_request_start(
            endpoint=self.settings.api_address,
            request_data={
                "service": "Models_GetVoiceCloningModels",
                "query_type": "voice_cloning_models"
            },
            auth_present=bool(metadata)
        )
        
        start_time = time.time()
        
        try:
            # Mock implementation - replace with actual when available
            models = [
                {
                    "name": "voice_cloning_v1",
                    "description": "Voice cloning model v1",
                    "languages": ["ru-RU", "en-US"],
                    "sample_rate": 22050
                }
            ]
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Log success
            self.logger.log_request_success(
                request_id=request_id,
                response_size=len(str(models).encode()),
                duration_ms=duration_ms
            )
            
            # Log models specific data
            self.logger.log_system_event("voice_cloning_models_query_success", 
                f"Voice cloning models retrieved: {len(models)} models", {
                    "request_id": request_id,
                    "models_count": len(models),
                    "model_names": [model.get('name', 'unknown') for model in models],
                    "processing_time_ms": duration_ms
                })
            
            return models
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            self.logger.log_request_error(
                request_id=request_id,
                error=e,
                duration_ms=duration_ms
            )
            
            raise
    
    def get_all_models(self, timeout: float = 60.0) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all available models (TTS, ASR, Voice Cloning) with comprehensive logging.
        
        Args:
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary with all model types
            
        Raises:
            Exception: If any model query fails
        """
        self.logger.log_system_event("all_models_query_start", "Starting comprehensive models query")
        
        all_models = {}
        total_start_time = time.time()
        
        try:
            # Get TTS models
            all_models["tts"] = self.get_tts_models(timeout=timeout/3)
            
            # Get ASR models
            all_models["asr"] = self.get_asr_models(timeout=timeout/3)
            
            # Get Voice Cloning models
            all_models["voice_cloning"] = self.get_voice_cloning_models(timeout=timeout/3)
            
            total_duration_ms = (time.time() - total_start_time) * 1000
            
            # Log comprehensive summary
            self.logger.log_system_event("all_models_query_success", 
                "All models retrieved successfully", {
                    "tts_models_count": len(all_models["tts"]),
                    "asr_models_count": len(all_models["asr"]),
                    "voice_cloning_models_count": len(all_models["voice_cloning"]),
                    "total_models": sum(len(models) for models in all_models.values()),
                    "total_processing_time_ms": total_duration_ms
                })
            
            return all_models
            
        except Exception as e:
            total_duration_ms = (time.time() - total_start_time) * 1000
            
            self.logger.log_system_event("all_models_query_failed", 
                f"Models query failed: {e}", {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "total_processing_time_ms": total_duration_ms,
                    "partial_results": all_models
                })
            
            raise
    
    def close(self):
        """Close the gRPC channel and log shutdown."""
        if self.channel:
            self.channel.close()
            self.logger.log_system_event("models_client_shutdown", "Models service client closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def test_logged_models(config_path: str):
    """
    Test function for logged models service operations.
    
    Args:
        config_path: Path to configuration file
    """
    logger = get_logger()
    
    logger.log_system_event("models_test_start", "Starting logged models service test", {
        "config_path": config_path
    })
    
    try:
        with LoggedModelsClient(config_path) as client:
            # Test all models query
            all_models = client.get_all_models()
            
            logger.log_system_event("models_test_success", 
                f"Models service test completed successfully", {
                    "total_models": sum(len(models) for models in all_models.values()),
                    "model_types": list(all_models.keys())
                })
            
            return all_models
            
    except Exception as e:
        logger.log_system_event("models_test_failed", f"Models service test failed: {e}", {
            "error": str(e),
            "error_type": type(e).__name__
        })
        raise
