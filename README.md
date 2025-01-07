# YouTube Downloader

This project allows you to download YouTube videos and audio using `yt-dlp`. The downloaded files are saved in separate directories for audio and video.

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

1. Run the [yt.py](http://_vscodecontentref_/0) script:
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
    - Audio: [yt_downloaded_audio](http://_vscodecontentref_/1)
    - Video: [yt_downloaded_videos](http://_vscodecontentref_/2)

License
This project is licensed under the MIT License.
