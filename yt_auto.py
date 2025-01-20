import yt_dlp
import os
import time

def download_video(link, download_type):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if download_type == 1:  # Audio download
        output_dir = os.path.join(current_dir, 'yt_downloaded_audio')
        save_dist_path = os.path.join(output_dir, '%(title)s.%(ext)s')
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': save_dist_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    elif download_type == 2:  # Video download
        output_dir = os.path.join(current_dir, 'yt_downloaded_videos')
        save_dist_path = os.path.join(output_dir, '%(title)s.%(ext)s')
        ydl_opts = {
            'outtmpl': save_dist_path,
            'merge_output_format': 'mp4'
        }

    try:
        os.makedirs(output_dir, exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        print("Download completed")

    except Exception as e:
        print(f"Error: {e}")


def get_latest_video_url(channel_url):
    ydl_opts = {
        'extract_flat': True,
        'force_generic_extractor': True,
        'playlistend': 1,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        if 'entries' in info:
            latest_video = info['entries'][0]
            return latest_video['url']
        else:
            raise Exception("No videos found in the channel.")


def monitor_channel(channel_url, download_type, interval=3600):
    downloads_file_txt = "latest_downloads.txt"

    while True:
        try:
            latest_video_url = get_latest_video_url(channel_url)

            try:
                with open(downloads_file_txt, "r") as f:
                    last_downloaded_url = f.readline().strip()
            except FileNotFoundError:
                last_downloaded_url = None  # No previous downloads recorded

            if latest_video_url != last_downloaded_url:
                print(f"New video found: {latest_video_url}")
                print(last_downloaded_url)
                download_video(latest_video_url, download_type)

                with open(downloads_file_txt, "w") as f:
                    f.write(latest_video_url)
                    
                print("File updated with the latest video URL.")
            else:
                print("No new videos found.")
        except Exception as e:
            print(f"Error monitoring channel: {e}")

        time.sleep(interval)

try:
    channel_url = input("Enter the YouTube channel URL: ")
    download_type = int(input("How Do You Want to Download it: \n 1. Audio\n 2. Video\n"))
    if download_type not in [1, 2]:
        raise ValueError("Invalid download type. Please enter 1 for Audio or 2 for Video.")
    interval = int(input("Check interval in seconds (e.g., 3600 for 1 hour): "))
except ValueError as e:
    print(f"Invalid input: {e}")
    exit(1)

monitor_channel(channel_url, download_type, interval)