import yt_dlp
import os
import shutil

def download_video(link, download_type, save_dist):

    save_dist_path = "/home/kbassem/Videos/Youtube_Downloads/%(title)s"

    try:
        if download_type == 1:  # Audio download
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': f'{save_dist_path}',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }
        elif download_type == 2:  # Video download
            ydl_opts = {
                'outtmpl': f'{save_dist_path}',
                'merge_output_format': 'mp4'
            }

        # Ensure the directory exists
        output_dir = '/home/kbassem/Videos/Youtube_Downloads/'
        os.makedirs(output_dir, exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        '''if save_dist == 2:
            server_path = "/run/user/1000/gvfs/smb-share:server=kb-imac.local,share=kb/Videos/Youtube_Download"
            shutil.move(save_dist_path, server_path)'''
        print("Download completed")

    except Exception as e:
        print(f"Error: {e}")

link = input("Link: ")
download_type = int(input("How Do You Want to Download it: \n 1. Audio\n 2. Video\n"))
save_dist = int(input("Where to save the file: \n 1. Device\n 2. Server\n"))
download_video(link, download_type, save_dist)
