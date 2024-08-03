import yt_dlp as youtube_dl

def download_video(link):
    try:
        ydl_opts = {
                    'outtmpl': '/mnt/d/Videos/Youtube_Downloads/%(title)s.%(ext)s',
                    'format': 'best',
                }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Download completed")
    except Exception as e:
        print(f"Error: {e}")

link = input("Link: ")
download_video(link)
