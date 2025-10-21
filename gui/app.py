import customtkinter as ctk
import threading
import os
from tkinter import filedialog, messagebox
import webbrowser
from config import *
from utils.ffmpeg_handler import setup_ffmpeg_env
from utils.platform_detector import detect_platform
from core.downloader import Downloader
from gui.components import create_sidebar, create_url_card, create_options_card
from gui.components import create_location_card, create_progress_card

class TheVUnitDownloader:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title(APP_NAME)
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(False, False)

        try:
            icon_path = os.path.join(os.getcwd(), "assets", "thevunit_logo.ico")
            if os.path.exists(icon_path):
                self.window.iconbitmap(icon_path)
        except:
            pass
        ctk.set_appearance_mode(DEFAULT_THEME)
        ctk.set_default_color_theme(DEFAULT_COLOR_THEME)
        self.download_path = DEFAULT_DOWNLOAD_PATH
        os.makedirs(self.download_path, exist_ok=True)
        setup_ffmpeg_env()
        
        self.downloader = Downloader(progress_callback=self.update_progress)
        
        self.create_ui()
    
    def show_update_dialog(self, version, url):
        if messagebox.askyesno("Update Available", 
            f"New version {version} available!\nCurrent: {APP_VERSION}\n\nDownload now?"):
            if url:
                webbrowser.open(url)
    
    def create_ui(self):
        self.sidebar = create_sidebar(
            self.window,
            on_theme_toggle=self.toggle_theme,
            on_supported_sites=self.show_supported_sites,
            on_about=self.show_about,
            on_github=lambda: webbrowser.open(GITHUB_URL)
        )
        main_area = ctk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        main_area.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        header = ctk.CTkLabel(
            main_area,
            text=APP_NAME,
            font=ctk.CTkFont(size=28, weight="bold")
        )
        header.pack(pady=(0, 5))
        
        subtitle = ctk.CTkLabel(
            main_area,
            text="Download from YouTube, Instagram, TikTok, Facebook & 1000+ sites",
            font=ctk.CTkFont(size=13),
            text_color=("gray50", "gray60")
        )
        subtitle.pack(pady=(0, 30))
        
        self.url_entry, self.platform_label = create_url_card(
            main_area,
            on_url_change=self.on_url_change
        )
        self.type_var, self.format_var, self.quality_var, self.quality_menu = create_options_card(
            main_area,
            on_format_change=self.on_format_change
        )
        self.path_entry = create_location_card(
            main_area,
            default_path=self.download_path,
            on_browse=self.browse_folder
        )
        self.progress_bar, self.status_label = create_progress_card(main_area)
        self.download_btn = ctk.CTkButton(
            main_area,
            text="Start Download",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=55,
            corner_radius=10,
            fg_color=(PRIMARY_COLOR, PRIMARY_COLOR),
            hover_color=(PRIMARY_HOVER, PRIMARY_HOVER),
            command=self.start_download
        )
        self.download_btn.pack(fill="x", pady=20)
    
    def on_url_change(self, event):
        url = self.url_entry.get().strip()
        if url:
            platform = detect_platform(url)
            self.platform_label.configure(text=f"✓ {platform}")
        else:
            self.platform_label.configure(text="")
    
    def on_format_change(self, value):
        if value == "Video":
            self.quality_menu.configure(state="normal")
        else:
            self.quality_menu.configure(state="disabled")
    
    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        new_mode = "light" if current == "Dark" else "dark"
        ctk.set_appearance_mode(new_mode)
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path = folder
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, folder)
    
    def show_supported_sites(self):
        sites_text = "Supported Platforms:\n\n"
        sites_text += "\n".join([f"✓ {site}" for site in SUPPORTED_SITES])
        sites_text += "\n\n+ 1000+ more websites supported by yt-dlp!"
        messagebox.showinfo("Supported Sites", sites_text)
    
    def show_about(self):
        messagebox.showinfo(
            f"About {APP_NAME}",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "Multi-platform video downloader supporting:\n"
            "YouTube, Instagram, TikTok, Facebook,\n"
            "Twitter, Vimeo, and 1000+ sites.\n\n"
            f"Developed by {DEVELOPER}"
        )
    
    def update_progress(self, value, text):
        self.window.after(0, lambda: self.progress_bar.set(value))
        self.window.after(0, lambda: self.status_label.configure(text=text))
    
    def download_content(self):
        url = self.url_entry.get().strip()
        
        if not url:
            self.window.after(0, lambda: messagebox.showerror("Error", "Please enter a video URL"))
            return

        self.window.after(0, lambda: self.download_btn.configure(
            state="disabled", 
            text="⏳ Downloading..."
        ))
        self.window.after(0, lambda: self.progress_bar.set(0))
        
        format_type = self.format_var.get()
        quality = self.quality_var.get()
        is_playlist = (self.type_var.get() == "Playlist")
        result = self.downloader.download(
            url=url,
            download_path=self.download_path,
            format_type=format_type,
            quality=quality,
            is_playlist=is_playlist
        )
        
        if result['success']:
            self.window.after(0, lambda: messagebox.showinfo("Success", result['message']))
        else:
            self.window.after(0, lambda: messagebox.showerror("Download Error", result['message']))
        
        self.window.after(0, lambda: self.download_btn.configure(
            state="normal", 
            text="Start Download"
        ))
        self.window.after(0, lambda: self.progress_bar.set(0))
    
    def start_download(self):
        thread = threading.Thread(target=self.download_content, daemon=True)
        thread.start()
    
    def run(self):
        self.window.mainloop()