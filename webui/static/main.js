document.getElementById('download-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    document.getElementById('loading').style.display = 'block';
    document.getElementById('progress-container').style.display = 'block';
    document.getElementById('message').innerText = '';

    fetch('/download', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('progress-container').style.display = 'none';
        document.getElementById('message').innerText = data.message;
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('progress-container').style.display = 'none';
        document.getElementById('message').innerText = 'Error: ' + error;
    });
});

const socket = io();
socket.on('progress', function(data) {
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    progressBar.style.width = data.percent + '%';
    progressText.innerText = data.percent + '%';
});