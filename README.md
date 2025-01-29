# YouTube Downloader

This project allows you to download YouTube videos and audio using `yt-dlp`. The downloaded files are saved in separate directories for audio and video. Additionally, you can monitor a YouTube channel for new videos and automatically download them.

## Installation

1. Clone the repository from GitHub:
    ```sh
    git clone https://github.com/kbassem10/yt.git
    cd yt
    ```

2. Install the required dependencies:
    ```sh
    pip install yt-dlp
    ```

## Usage

### Manual Download

1. Run the [yt.py](yt.py) script:
    ```sh
    python yt.py
    ```
    or
    ```sh
    python3 yt.py
    ```

2. Enter the YouTube link when prompted:
    ```
    Link: <your-youtube-link>
    ```

3. Choose the download type:
    ```
    How Do You Want to Download it: 
     1. Audio
     2. Video
    ```

4. The downloaded files will be saved in the following directories:
    - Audio: [yt_downloaded_audio](yt_downloaded_audio)
    - Video: [yt_downloaded_videos](yt_downloaded_videos)

### Automatic Channel Monitoring

1. Run the [yt_auto.py](yt_auto.py) script:
    ```sh
    python yt_auto.py
    ```
    or
    ```sh
    python3 yt_auto.py
    ```

2. Enter the YouTube channel URL when prompted:
    ```
    Enter the YouTube channel URL: <your-channel-url>
    ```

3. Choose the download type:
    ```
    How Do You Want to Download it: 
     1. Audio
     2. Video
    ```

4. Enter the check interval in seconds (e.g., 3600 for 1 hour):
    ```
    Check interval in seconds (e.g., 3600 for 1 hour): <interval>
    ```

5. The script will monitor the channel for new videos and download them automatically. The downloaded files will be saved in the following directories:
    - Audio: [yt_downloaded_audio](yt_downloaded_audio)
    - Video: [yt_downloaded_videos](yt_downloaded_videos)

## License

This project is licensed under the MIT License.