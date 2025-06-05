document.getElementById('download-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    document.getElementById('loading').style.display = 'block';
    document.getElementById('message').innerText = 'Preparing download...';

    try {
        const response = await fetch('/get_info', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('message').innerText = 'Starting download...';

            // Create and trigger download
            const downloadLink = document.createElement('a');
            downloadLink.href = data.url;
            downloadLink.download = `${data.title}.${data.ext}`;
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
    }
});