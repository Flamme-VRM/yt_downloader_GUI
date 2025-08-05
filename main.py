import yt_dlp
import logging
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('download.log'), logging.StreamHandler()]
)

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("Download completed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

def get_video_url():
    try:
        url = input("Enter the video URL: ")
        logging.info(f"Received URL: {url}")
        if not url:
            raise ValueError("URL cannot be empty")
            logging.error(f"Could not download video: URL is empty")
        if not url.startswith("http"):
            raise ValueError("Invalid URL format. Must start with 'http' or 'https'")
            logging.error(f"Could not download video: Invalid URL format - {url}")
        print("✓ URL is valid")
        return url 
    except ValueError as ve:
        print(f"✗ URL validation failed: {ve}")
        return None

class VideoDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
        self.root.geometry("500x200")
        self.root.resizable(False, False)
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # URL input section
        ttk.Label(main_frame, text="Video URL:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        url_frame = ttk.Frame(main_frame)
        url_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        self.clear_button = ttk.Button(url_frame, text="Clear", command=self.clear_url)
        self.clear_button.grid(row=0, column=1)
        
        # Download buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, pady=(0, 10))
        
        self.download_button = ttk.Button(buttons_frame, text="Download", command=self.start_video_download)
        self.download_button.grid(row=0, column=0, padx=(0, 10))
        
        self.mp3_button = ttk.Button(buttons_frame, text="MP3 Only", command=self.start_audio_download)
        self.mp3_button.grid(row=0, column=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to download")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, sticky=tk.W)
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        url_frame.columnconfigure(0, weight=1)
    
    def clear_url(self):
        self.url_var.set("")
    
    def start_video_download(self):
        url = self.url_var.get().strip()
        if not self.validate_url(url):
            return
        
        # Disable buttons during download
        self.download_button.config(state="disabled")
        self.mp3_button.config(state="disabled")
        self.status_var.set("Downloading video...")
        self.progress_var.set(0)
        
        # Start video download in separate thread
        download_thread = threading.Thread(target=self.download_video_gui, args=(url, False))
        download_thread.daemon = True
        download_thread.start()
    
    def start_audio_download(self):
        url = self.url_var.get().strip()
        if not self.validate_url(url):
            return
        
        self.download_button.config(state="disabled")
        self.mp3_button.config(state="disabled")
        self.status_var.set("Downloading audio...")
        self.progress_var.set(0)
        
        download_thread = threading.Thread(target=self.download_video_gui, args=(url, True))
        download_thread.daemon = True
        download_thread.start()
    
    def validate_url(self, url):
        if not url:
            messagebox.showerror("Error", "URL cannot be empty")
            return False
        
        if not url.startswith("http"):
            messagebox.showerror("Error", "Invalid URL format. Must start with 'http' or 'https'")
            return False
        
        return True
    
    def download_video_gui(self, url, audio_only=False):
        try:
            self.download_video_with_progress(url, audio_only)
            self.root.after(0, self.download_complete)
        except Exception as e:
            self.root.after(0, self.download_error, str(e))
    
    def download_complete(self):
        self.status_var.set("Download completed successfully!")
        self.progress_var.set(100)
        self.download_button.config(state="normal")
        self.mp3_button.config(state="normal")
        messagebox.showinfo("Success", "Download completed successfully!")
    
    def download_video_with_progress(self, url, audio_only=False):
        # Get system Downloads folder
        downloads_path = str(Path.home() / "Downloads")
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d:
                    progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    self.root.after(0, lambda: self.progress_var.set(progress))
                elif 'total_bytes_estimate' in d:
                    progress = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                    self.root.after(0, lambda: self.progress_var.set(progress))
        
        if audio_only:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(downloads_path, '%(title)s_audio.%(ext)s'),
                'noplaylist': True,
                'progress_hooks': [progress_hook],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'postprocessor_args': ['-ar', '44100'],
            }
            download_type = "audio"
        else:
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'progress_hooks': [progress_hook],
            }
            download_type = "video"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logging.info(f"Starting {download_type} download from URL: {url}")
            ydl.download([url])
            logging.info(f"{download_type.capitalize()} downloaded successfully from URL: {url}")
    
    def download_error(self, error_msg):
        self.status_var.set("Download failed")
        self.progress_var.set(0)
        self.download_button.config(state="normal")
        self.mp3_button.config(state="normal")
        logging.error(f"Download failed: {error_msg}")
        messagebox.showerror("Download Error", f"An error occurred: {error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderGUI(root)
    root.mainloop()
    
# This is now a GUI-based video downloader using yt-dlp with tkinter interface.