from typing import List, Optional
from pydantic import BaseModel


class Request(BaseModel):
    request_id: str
    audio_id: str
    status: str
    timestamp: str


class GetRequestsResponse(BaseModel):
    requests: List[Request]


class TranscriptItem(BaseModel):
    start_time: float
    end_time: float
    transcript: str
    confidence: float


class GetTranscriptResponse(BaseModel):
    transcript: List[TranscriptItem]


class VadItem(BaseModel):
    start_time: float
    end_time: float


class GetVadResponse(BaseModel):
    vad: List[VadItem]
