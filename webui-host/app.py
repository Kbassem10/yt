from flask import Flask, render_template, request, jsonify, send_from_directory
import yt_dlp

app = Flask(__name__)

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

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        raise Exception(f"Failed to get video info: {str(e)}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

@app.route("/get_info", methods=["POST"])
def get_info():
    try:
        yt_url = request.form.get("yt_url")
        download_type = request.form.get("download_type")
        
        if not yt_url:
            return jsonify({"error": "No URL provided"}), 400
            
        info = get_video_info(yt_url, download_type)
        
        return jsonify({
            "title": info['title'],
            "url": info['url'],
            "ext": "mp3" if download_type == "1" else "mp4"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
