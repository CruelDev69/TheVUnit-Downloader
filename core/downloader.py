import os
import yt_dlp
from utils.ffmpeg_handler import get_ffmpeg_path
from utils.platform_detector import detect_platform

class Downloader:
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
    
    def progress_hook(self, d):
        if not self.progress_callback:
            return
            
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                
                if total > 0:
                    percent = (downloaded / total) * 100
                    self.progress_callback(percent/100, f"Downloading... {percent:.1f}%")
                else:
                    speed = d.get('speed', 0)
                    if speed:
                        speed_mb = speed / (1024 * 1024)
                        self.progress_callback(0.5, f"Downloading... {speed_mb:.1f} MB/s")
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_callback(1, "Processing... Please wait")
    
    def download(self, url, download_path, format_type="Video", quality="Best", is_playlist=False):
        platform = detect_platform(url)
        
        if self.progress_callback:
            self.progress_callback(0.1, f"Connecting to {platform}...")
        
        try:
            ydl_opts = {
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': False,
                'nocheckcertificate': True,
            }
            
            if 'instagram.com' in url.lower() or 'tiktok.com' in url.lower():
                ydl_opts['http_headers'] = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            if format_type == "Audio Only":
                ffmpeg_path = get_ffmpeg_path()
                
                if not ffmpeg_path:
                    return {
                        'success': False,
                        'message': "FFmpeg not found! Please check FFmpeg installation.",
                        'title': None
                    }
                
                print(f"Using FFmpeg at: {ffmpeg_path}")
                
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'prefer_ffmpeg': True,
                })
                ffmpeg_dir = os.path.dirname(ffmpeg_path)
                if ffmpeg_dir and os.path.isdir(ffmpeg_dir):
                    os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
                
            else:
                if quality == "Best":
                    ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best'
                else:
                    height = quality.replace('p', '')
                    ydl_opts['format'] = f'bestvideo[ext=mp4][height<={height}]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best[ext=mp4][height<={height}]/best'
                
                ydl_opts['merge_output_format'] = 'mp4'
                ffmpeg_path = get_ffmpeg_path()
                if ffmpeg_path:
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }]
                    ydl_opts['postprocessor_args'] = [
                        '-c:v', 'libx264',
                        '-c:a', 'aac',
                        '-crf', '23',
                        '-preset', 'medium',
                        '-profile:v', 'high',
                        '-level', '4.0',
                        '-pix_fmt', 'yuv420p',
                        '-movflags', '+faststart',
                        '-strict', 'experimental'
                    ]
                    
                    ffmpeg_dir = os.path.dirname(ffmpeg_path)
                    if ffmpeg_dir and os.path.isdir(ffmpeg_dir):
                        os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
                    
                    print(f"Using FFmpeg for video conversion: {ffmpeg_path}")
            
            if is_playlist and platform == "YouTube":
                ydl_opts['noplaylist'] = False
            else:
                ydl_opts['noplaylist'] = True
    
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                
                if self.progress_callback:
                    self.progress_callback(0.2, f"Found: {title[:50]}...")
                
                ydl.download([url])
            
            if self.progress_callback:
                self.progress_callback(1, "✅ Download completed!")
            
            return {
                'success': True,
                'message': f"Download completed successfully!\n\nSaved to:\n{download_path}",
                'title': title
            }
            
        except Exception as e:
            error_msg = self._format_error(str(e), get_ffmpeg_path())
            
            if self.progress_callback:
                self.progress_callback(0, "❌ Download failed")
            
            return {
                'success': False,
                'message': error_msg,
                'title': None
            }
    
    def _format_error(self, error_msg, ffmpeg_path):
        if "ffmpeg" in error_msg.lower() or "codec" in error_msg.lower():
            if ffmpeg_path:
                return (f"Video conversion failed!\n\n"
                       f"FFmpeg Path: {ffmpeg_path}\n\n"
                       f"Error: {error_msg[:100]}\n\n"
                       f"Solutions:\n"
                       f"1. Redownload FFmpeg from ffmpeg.org\n"
                       f"2. Try different quality/platform\n"
                       f"3. Check if ffmpeg.exe is not corrupted")
            else:
                return ("FFmpeg not found!\n\n"
                       f"Video will download but may need codec to play.\n\n"
                       "To fix permanently:\n"
                       "1. Download FFmpeg from https://ffmpeg.org\n"
                       "2. Extract ffmpeg.exe to 'assets' folder\n"
                       "3. Restart app\n\n"
                       "Videos will be converted to compatible MP4 format.")
        elif "private" in error_msg.lower():
            return "This video is private or restricted.\nPlease check the URL and try again."
        elif "copyright" in error_msg.lower():
            return "This video may have copyright restrictions.\nTry a different quality or format."
        elif "not available" in error_msg.lower():
            return "Video not available in your region\nor the URL is incorrect."
        else:
            return (f"Download failed!\n\n"
                   f"Error: {error_msg[:200]}\n\n"
                   f"Try:\n- Different quality\n- Different URL\n- Check internet connection")