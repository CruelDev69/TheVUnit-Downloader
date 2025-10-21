import os
import sys
import subprocess

def get_ffmpeg_path():
    possible_paths = [
        os.path.join(os.getcwd(), "assets", "ffmpeg.exe"),
        os.path.join(os.getcwd(), "ffmpeg.exe"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "ffmpeg.exe"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ffmpeg.exe"),
        os.path.join(os.path.dirname(sys.executable), "assets", "ffmpeg.exe"),
        os.path.join(os.path.dirname(sys.executable), "ffmpeg.exe"),
        "ffmpeg.exe",
    ]
    
    for path in possible_paths:
        if os.path.isfile(path):
            try:
                result = subprocess.run([path, "-version"], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
                if result.returncode == 0:
                    print(f"FFmpeg found at: {path}")
                    return os.path.abspath(path)
            except Exception as e:
                print(f"Error checking {path}: {e}")
                continue
    
    print("FFmpeg not found in any location")
    return None

def setup_ffmpeg_env():
    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path:
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        if ffmpeg_dir and os.path.isdir(ffmpeg_dir):
            current_path = os.environ.get('PATH', '')
            if ffmpeg_dir not in current_path:
                os.environ['PATH'] = ffmpeg_dir + os.pathsep + current_path
            print(f"✅ FFmpeg loaded from: {ffmpeg_path}")
        else:
            os.environ['PATH'] = os.getcwd() + os.pathsep + os.environ.get('PATH', '')
            print(f"✅ FFmpeg loaded from: {ffmpeg_path}")
        return True
    else:
        print("⚠️ FFmpeg not found - Audio conversion will not work")
        return False