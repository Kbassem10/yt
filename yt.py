import yt_dlp
import os
import shutil

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

    # try:
    #     import yt_1
    #     yt_1.move_file(output_dir)
    # except Exception as e:
    #     print(f"Error: {e}")

    try:
        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        print("Download completed")

    except Exception as e:
        print(f"Error: {e}")

link = input("Link: ")
download_type = int(input("How Do You Want to Download it: \n 1. Audio\n 2. Video\n"))
download_video(link, download_type)