from datetime import datetime

from pydantic import BaseModel


class Request(BaseModel):
    request_id: str
    session_id: str | None = None
    trace_id: str | None = None
    created_at: datetime


class RequestsList(BaseModel):
    data: list[Request]


class Duration(BaseModel):
    seconds: int = 0
    nanos: int

    def __str__(self) -> str:
        secs = self.seconds + self.nanos / 1e9
        return f"{secs:05.2f}"


class Word(BaseModel):
    word: str
    confidence: float
    start_time: Duration
    end_time: Duration


class Transcript(BaseModel):
    transcript: str
    confidence: float
    words: list[Word]
    start_time: Duration
    end_time: Duration


class TranscriptList(BaseModel):
    data: list[Transcript]


class VAMark(BaseModel):
    mark_type: str
    offset_ms: int


class VAMarkList(BaseModel):
    data: list[VAMark]
