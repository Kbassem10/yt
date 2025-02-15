document.getElementById('download-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    // Show loading state
    const loadingEl = document.getElementById('loading');
    const messageEl = document.getElementById('message');
    loadingEl.style.display = 'block';
    messageEl.innerText = 'Preparing download...';

    try {
        const response = await fetch('/get_info', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            messageEl.innerText = 'Starting download...';
            
            // Create and trigger download
            const downloadLink = document.createElement('a');
            downloadLink.href = data.url;
            downloadLink.download = `${data.title}.${data.ext}`;
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
            
            messageEl.innerText = 'Download started!';
        } else {
            throw new Error(data.error || 'Failed to get video information');
        }
    } catch (error) {
        messageEl.innerText = 'Error: ' + error.message;
    } finally {
        loadingEl.style.display = 'none';
    }
});