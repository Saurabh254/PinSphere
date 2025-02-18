__all__ = ["FileContentType"]
from enum import Enum


class FileContentType(Enum):
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    MP4 = "video/mp4"
    WEBM = "video/webm"
    MP3 = "audio/mpeg"
    WAV = "audio/wav"
    OGG = "audio/ogg"
