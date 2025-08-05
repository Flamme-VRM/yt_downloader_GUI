# AutoPosting Video Downloader

A Python-based video downloader utility that allows users to easily download videos from various platforms using yt-dlp. Features URL validation, logging capabilities, and error handling.

## Features
- Video downloading using yt-dlp
- URL validation and error handling
- Logging system for tracking downloads and errors
- Support for various video platforms
- Easy-to-use command line interface

## Requirements
- Python 3.x
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
Run the script:
```bash
python main.py
```
Then enter the video URL when prompted.

## Logging
All download activities are logged in `download.log` file, including:
- Video download attempts
- Successful downloads
- Errors and exceptions