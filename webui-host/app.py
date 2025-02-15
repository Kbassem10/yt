from flask import Flask, render_template, request, jsonify
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
            # Add browser headers
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            'cookiesfrombrowser': ('chrome',),  # Use cookies from Chrome
            'nocheckcertificate': True,
        }
    else:  # Video
        ydl_opts = {
            'format': 'best',
            'merge_output_format': 'mp4',
            # Add browser headers
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            'cookiesfrombrowser': ('chrome',),  # Use cookies from Chrome
            'nocheckcertificate': True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        # More detailed error handling
        error_message = str(e)
        if "Sign in to confirm you're not a bot" in error_message:
            raise Exception("YouTube is blocking automated access. Please try again later or contact support.")
        elif "Video unavailable" in error_message:
            raise Exception("This video is unavailable or private.")
        else:
            raise Exception(f"Failed to get video info: {error_message}")

@app.route("/")
def index():
    return render_template("index.html")

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)