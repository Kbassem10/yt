from flask import Flask, render_template, request
import os
import yt_dlp

app = Flask(__name__)

def download_video(link, download_type):
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Change to parent directory

    if download_type == '1':  # Audio download
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
    elif download_type == '2':  # Video download
        output_dir = os.path.join(current_dir, 'yt_downloaded_videos')
        save_dist_path = os.path.join(output_dir, '%(title)s.%(ext)s')
        ydl_opts = {
            'outtmpl': save_dist_path,
            'merge_output_format': 'mp4'
        }
    else:
        raise ValueError("Invalid download type")

    try:
        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        print("Download completed")

    except Exception as e:
        print(f"Error: {e}")
        raise

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    yt_url = request.form.get("yt_url")
    download_type = request.form.get("download_type")

    try:
        download_video(yt_url, download_type)
        return render_template("index.html", done="Download completed")
    
    except Exception as e:
        return render_template("index.html", error=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)