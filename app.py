from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import os

app = Flask(__name__)

# Directory to save resized images
UPLOAD_FOLDER = 'static/resized_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """
    Render the home page with the upload form.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Handle image upload and pixel resizing.
    """
    try:
        # Get the uploaded file
        image_file = request.files['image']
        if not image_file:
            return "No file uploaded!", 400

        # Get desired pixel size
        pixels = int(request.form['pixels'])

        # Open the image using Pillow
        img = Image.open(image_file)

        # Calculate new dimensions to match the specified pixel size
        aspect_ratio = img.width / img.height

        # If the image's total pixel count is greater than the target, resize it
        if img.width * img.height > pixels:
            # Calculate new dimensions based on the aspect ratio
            new_width = int((pixels * aspect_ratio) ** 0.5)
            new_height = int((pixels / aspect_ratio) ** 0.5)

            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        else:
            resized_img = img  # If image is smaller than the target size, keep it as is

        # Save the resized image with explicit format
        filename = f"resized_{image_file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        resized_img.save(filepath, format='JPEG')

        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)