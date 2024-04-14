import tkinter as tk
from tkinter import messagebox
from pytube import YouTube, Playlist
from customtkinter import *
import threading
import os
import time
import re
from PIL import Image, ImageTk

class DownloadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TheVUnit Downloader")
        self.root.iconbitmap(f"{os.getcwd()}/Assets/icon.ico")
        self.root.geometry("920x600")
        self.root.resizable(False, False)
        self.dark_mode = tk.BooleanVar(value=False)
        self.root.option_add("*Font", "HelveticaNeue 10")
        self.buttons = []
        self.widgets = []
        self.create_widgets()

    def create_widgets(self):
        title = CTkLabel(self.root,text="TheVUnit Downloader", font=("HelveticaNeue", 30), bg_color="transparent")
        title.pack(padx = 10, pady = 10)

        # Entry for URL
        url_entry = CTkEntry(self.root, width=500, font=("HelveticaNeue", 10), placeholder_text="Enter a YouTube URL")
        self.buttons.append(url_entry)
        url_entry.pack(pady=10)

        # FileType Radio Buttons
        file_type_frame = CTkFrame(self.root)
        file_type_frame.pack(pady=10)
        self.widgets.append(file_type_frame)
        file_type_var = tk.StringVar(value="video")


        audio_radio = CTkRadioButton(file_type_frame, text="Audio", variable=file_type_var, value="audio", fg_color="#1900FF")
        audio_radio.grid(row=0, column=0, padx=10)
        self.buttons.append(audio_radio)

        video_radio = CTkRadioButton(file_type_frame, text="Video", variable=file_type_var, value="video", fg_color="#1900FF")
        video_radio.grid(row=0, column=1, padx=10)
        self.buttons.append(video_radio)

        # LinkType Radio Buttons
        link_type_frame = CTkFrame(self.root)
        link_type_frame.pack(pady=10)
        self.widgets.append(link_type_frame)
        link_type_var = tk.StringVar(value="single")

        single_radio = CTkRadioButton(link_type_frame, text="Single", variable=link_type_var, value="single", fg_color="#1900FF")
        single_radio.grid(row=0, column=0, padx=10)
        self.buttons.append(single_radio)

        playlist_radio = CTkRadioButton(link_type_frame, text="Playlist", variable=link_type_var, value="playlist", fg_color="#1900FF")
        playlist_radio.grid(row=0, column=1, padx=10)
        self.buttons.append(playlist_radio)

        # Start Download Button
        start_button = CTkButton(self.root, text="Start Download", command=lambda: self.start_download(url_entry.get(), file_type_var.get(), link_type_var.get()), fg_color="#1900FF")
        start_button.pack(pady=10)
        self.buttons.append(start_button) 
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        progress_bar = CTkProgressBar(self.root, variable=self.progress_var, mode="determinate", bg_color="#1900FF")
        progress_bar.pack(pady=10)

        # Status Label
        self.status_var = tk.StringVar(value="Status: Idle")
        status_label = CTkLabel(self.root, textvariable=self.status_var, bg_color="transparent", text_color_disabled="")
        status_label.pack(pady=10)
        self.buttons.append(status_label)

        # Dark Mode Checkbox
        self.dark_mode_checkbox = CTkSwitch(self.root, text="Theme Mode", variable=self.dark_mode, command=self.toggle_dark_mode, fg_color="#1900FF")
        self.dark_mode_checkbox.pack(pady=10)
        self.buttons.append(self.dark_mode_checkbox)

        # Load and display the image
        tvu_img_data = Image.open(f"{os.getcwd()}/Assets/thevunit.gif")
        self.tvu_img = CTkImage(light_image=tvu_img_data, dark_image=tvu_img_data, size=(500, 200))
        image_label = CTkLabel(self.root, text= "",image=self.tvu_img, corner_radius=8)
        image_label.pack(side="top", padx=10, pady=10)
        


    def start_download(self, url, file_type, link_type):
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        threading.Thread(target=self.download_thread, args=(url, file_type, link_type), daemon=True).start()

    def download_thread(self, url, file_type, link_type):
        try:
            if link_type == "playlist":
                playlist = Playlist(url)
                for video_url in playlist.video_urls:
                    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", video_url)
                    if video_id_match:
                        video_id = video_id_match.group(1)
                        video_url = f"https://www.youtube.com/watch?v={video_id}"
                        yt = YouTube(video_url)

                        if file_type == "audio":
                            stream = yt.streams.filter(only_audio=True, abr="256kbps").first()
                            self.download_file(stream)
                            file_path = stream.download(f"{os.getcwd()}/Audios")
                            base, ext = os.path.splitext(file_path)
                            extenSion = base + '.mp3'
                            os.rename(file_path, extenSion)
                            self.status_var.set(f"Status: Downloaded to {file_path}")

                        elif file_type == "video":
                            stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()
                            self.download_file(stream)
                            file_path = stream.download(f"{os.getcwd()}/Videos")
                            self.status_var.set(f"Status: Downloaded to {file_path}")

                        self.status_var.set("Status: Download Complete")
            elif link_type == "single":
                yt = YouTube(url)

                if file_type == "audio":
                    stream = yt.streams.filter(only_audio=True, abr="256kbps").first()
                    self.download_file(stream)
                    file_path = stream.download(f"{os.getcwd()}/Audios")
                    base, ext = os.path.splitext(file_path)
                    extenSion = base + '.mp3'
                    os.rename(file_path, extenSion)
                    self.status_var.set(f"Status: Downloaded to {file_path}")

                elif file_type == "video":
                    stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()
                    self.download_file(stream)
                    file_path = stream.download(f"{os.getcwd()}/Videos")
                    self.status_var.set(f"Status: Downloaded to {file_path}")

                    self.status_var.set("Status: Download Complete")
        except Exception as e:
         self.status_var.set(f"Status: Error - {str(e)}")
         print(f"An error occurred: {str(e)}")
    

    def download_file(self, stream):
        self.status_var.set("Status: Downloading...")

        total_bytes = stream.filesize
        downloaded_bytes = 0
        start_time = time.time()

        while downloaded_bytes < total_bytes:
            downloaded_bytes = min(downloaded_bytes + 1024, total_bytes)
            progress_percentage = int((downloaded_bytes / total_bytes) * 100)
            
            elapsed_time = time.time() - start_time
            download_speed = int(downloaded_bytes / (1024 * elapsed_time)) if elapsed_time > 0 else 0

            self.progress_var.set(progress_percentage)
            self.status_var.set(f"Status: Downloading ({stream.title}) {progress_percentage}% | Speed: {download_speed} KB/s | Time Elapsed: {int(elapsed_time)}s")


    def toggle_dark_mode(self):
        if self.dark_mode.get():
            set_appearance_mode("light")
            self.dark_mode_checkbox.configure(text="Dark Mode")
        elif not self.dark_mode.get():
            set_appearance_mode("dark")
            self.dark_mode_checkbox.configure(text="Light Mode")


if __name__ == "__main__":
    root = CTk()
    app = DownloadApp(root)
    root.mainloop()
