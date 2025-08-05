# AutoPosting Video Downloader

A Python-based video downloader with Tkinter GUI that enables easy video downloads from various platforms using yt-dlp. Features real-time progress tracking, URL validation, pop-up error handling, automatic downloads to system Downloads folder, and comprehensive logging for download history.

## Features
- Modern GUI interface with Tkinter
- Real-time download progress tracking
- Video downloading using yt-dlp (best quality)
- URL validation with pop-up error messages
- Automatic downloads to system Downloads folder
- Comprehensive logging system for download history
- Clear button for easy URL management
- Support for various video platforms

## Requirements
- Python 3.x (with tkinter - included in most Python installations)
- yt-dlp
- requests
- python-dotenv

## Installation
1. Clone this repository
2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Launch the GUI application:
```bash
python main.py
```
1. Paste or type the video URL in the input field
2. Click "Download" to start downloading
3. Watch the progress bar for download status
4. Use "Clear" button to clear the URL field
5. Downloads are automatically saved to your system's Downloads folder

## Logging
All download activities are logged in `download.log` file, including:
- Video download attempts
- Successful downloads
- Errors and exceptions