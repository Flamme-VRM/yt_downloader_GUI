import yt_dlp
import logging

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

if __name__ == "__main__":
    video_url = get_video_url()
    if video_url:
        download_video(video_url)
        logging.info(f"Video downloaded from URL: {video_url}")
    else:
        print("No valid URL provided. Exiting.")
        logging.error("No valid URL provided. Exiting.")
        raise SystemExit()
# This code is a simple video downloader using yt-dlp with logging and URL validation.