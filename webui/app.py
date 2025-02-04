from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os
import yt_dlp
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Function to remove ANSI escape codes
def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1b\[([0-9;]*[mGKH])')
    return ansi_escape.sub('', text)

# Progress hook for yt-dlp
def progress_hook(d):
    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0%')  # Get the progress percentage string
        percent_str_clean = remove_ansi_escape_codes(percent_str)  # Remove ANSI escape codes
        percent = float(percent_str_clean.strip('%'))  # Convert to float
        socketio.emit('progress', {'percent': percent})  # Emit progress update

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
            }],
            'progress_hooks': [progress_hook]
        }
    elif download_type == '2':  # Video download
        output_dir = os.path.join(current_dir, 'yt_downloaded_videos')
        save_dist_path = os.path.join(output_dir, '%(title)s.%(ext)s')
        ydl_opts = {
            'outtmpl': save_dist_path,
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook]
        }
    else:
        raise ValueError("Invalid download type")

    try:
        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        return "Download completed"

    except Exception as e:
        return f"Error: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    yt_url = request.form.get("yt_url")
    download_type = request.form.get("download_type")

    message = download_video(yt_url, download_type)
    return jsonify({"message": message})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)