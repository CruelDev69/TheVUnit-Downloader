from .platform_detector import detect_platform
from .ffmpeg_handler import get_ffmpeg_path, setup_ffmpeg_env

__all__ = [
    'detect_platform',
    'get_ffmpeg_path',
    'setup_ffmpeg_env',
]