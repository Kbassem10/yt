document.getElementById('download-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    document.getElementById('loading').style.display = 'block';
    document.getElementById('progress-container').style.display = 'block';
    document.getElementById('message').innerText = '';

    try {
        // First get the video info and direct download URL
        const response = await fetch('/get_info', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Create a download link
            const downloadLink = document.createElement('a');
            downloadLink.href = data.url;
            downloadLink.download = `${data.title}.${data.ext}`;
            
            // Add the link to the document and click it
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
            
            document.getElementById('message').innerText = 'Download started!';
        } else {
            throw new Error(data.error || 'Failed to get video information');
        }
    } catch (error) {
        document.getElementById('message').innerText = 'Error: ' + error.message;
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('progress-container').style.display = 'none';
    }
});

const socket = io();
socket.on('progress', function(data) {
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    progressBar.style.width = data.percent + '%';
    progressText.innerText = data.percent + '%';
});