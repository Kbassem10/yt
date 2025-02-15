from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_video_info(url, download_type):
    # Common options for both audio and video
    common_opts = {
        'no_warnings': True,
        'quiet': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],  # Use android client
                'skip': ['dash', 'hls']  # Skip DASH and HLS manifests
            }
        }
    }

    if download_type == '1':  # Audio
        ydl_opts = {
            **common_opts,
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:  # Video
        ydl_opts = {
            **common_opts,
            'format': 'best[ext=mp4]',  # Prefer MP4 format
            'merge_output_format': 'mp4'
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        error_message = str(e)
        if "Sign in to confirm you're not a bot" in error_message:
            raise Exception("YouTube is blocking access. Please try again in a few minutes.")
        elif "Video unavailable" in error_message:
            raise Exception("This video is unavailable or private.")
        elif "Private video" in error_message:
            raise Exception("This video is private.")
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
        
        # Make sure we have the necessary info
        if not info.get('url'):
            raise Exception("Could not get download URL. Please try again.")
            
        return jsonify({
            "title": info.get('title', 'video'),
            "url": info['url'],
            "ext": "mp3" if download_type == "1" else "mp4"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)