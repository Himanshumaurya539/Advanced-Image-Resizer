document.getElementById('image').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const previewImg = document.getElementById('preview-img');
    const previewText = document.querySelector('.preview p');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            previewImg.style.display = 'block';
            previewText.style.display = 'none';
        };
        reader.readAsDataURL(file);
    } else {
        previewImg.style.display = 'none';
        previewText.style.display = 'block';
    }
});

document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    if (result.success) {
        const resizedImg = document.getElementById('resized-img');
        const downloadLink = document.getElementById('download-link');

        resizedImg.src = result.resized_image_url;
        resizedImg.style.display = 'block';
        downloadLink.href = result.resized_image_url;
        downloadLink.style.display = 'block';
    }
});
