import itertools
import wave
from collections.abc import Iterable


class AudioFile:
    def __init__(self, path: str) -> None:
        with wave.open(path, "rb") as audio:
            self._blob = audio.readframes(audio.getnframes())
            self._sample_rate = audio.getframerate()
            self._channels_count = audio.getnchannels()
            self._sample_size = audio.getsampwidth()

    @property
    def sample_rate(self) -> int:
        return self._sample_rate

    @property
    def channel_count(self) -> int:
        return self._channels_count

    @property
    def blob(self) -> bytes:
        return self._blob

    def chunks(self, chunk_len_ms: int) -> Iterable[bytes]:
        sample_rate_ms = self._sample_rate // 1000
        chunk_len = chunk_len_ms * sample_rate_ms * self._sample_size

        it = iter(self._blob)
        while True:
            chunk = bytes(itertools.islice(it, chunk_len))
            if not chunk:
                break
            yield chunk
