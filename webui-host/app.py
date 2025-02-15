from flask import Flask, Response, render_template, request, jsonify
# from flask_socketio import SocketIO, emit
import yt_dlp
import re
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
# socketio = SocketIO(app)

def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1b\[([0-9;]*[mGKH])')
    return ansi_escape.sub('', text)


# def progress_hook(d):
#     if d['status'] == 'downloading':
#         percent_str = d.get('_percent_str', '0%')
#         percent_str_clean = remove_ansi_escape_codes(percent_str)
#         percent = float(percent_str_clean.strip('%'))
#         socketio.emit('progress', {'percent': percent})

def get_video_info(url, download_type):
    if download_type == '1':  # Audio
        ydl_opts = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:  # Video
        ydl_opts = {
            'format': 'best',
            'merge_output_format': 'mp4',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_info", methods=["POST"])
def get_info():
    try:
        yt_url = request.form.get("yt_url")
        download_type = request.form.get("download_type")
        info = get_video_info(yt_url, download_type)
        
        return jsonify({
            "title": info['title'],
            "url": info['url'],
            "ext": "mp3" if download_type == "1" else "mp4"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)