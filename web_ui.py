"""
Web UI for Image Caption Generator with Enhanced Captions
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
import time
from io import BytesIO
from PIL import Image
import generate

def cleanup_file_with_retry(filepath, max_retries=3, delay=0.1):
    """
    Safely delete a file with retry logic to handle file lock issues
    """
    for attempt in range(max_retries):
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Successfully deleted temporary file: {filepath}")
                return True
        except (OSError, PermissionError) as e:
            print(f"Attempt {attempt + 1} failed to delete {filepath}: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))  # Exponential backoff
            else:
                print(f"Failed to delete {filepath} after {max_retries} attempts")
                return False
    return False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Set API key for enhancement
os.environ['GEMINI_API_KEY'] = 'AIzaSyAQCROVJ5EBdYuLxai_GMLx9OJgFZmoPbc'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            # Save the uploaded file temporarily
            filename = file.filename
            filepath = os.path.join('uploads', filename)
            
            # Create uploads directory if it doesn't exist
            os.makedirs('uploads', exist_ok=True)
            
            # Save file
            file.save(filepath)
            
            try:
                # Generate enhanced caption
                print(f"Processing image: {filepath}")
                original_caption, enhanced_caption = generate.getBothCaptions(filepath)
                
                return jsonify({
                    'success': True,
                    'enhanced_caption': enhanced_caption,
                    'original_caption': original_caption
                })
                
            finally:
                # Clean up the temporary file with retry logic
                cleanup_file_with_retry(filepath)
            
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/feature-image-image-captioning.webp')
def feature_image():
    return send_from_directory('.', 'feature-image-image-captioning.webp')

def cleanup_old_uploads():
    """
    Clean up old files in uploads directory that might be left over
    """
    uploads_dir = 'uploads'
    if os.path.exists(uploads_dir):
        try:
            for filename in os.listdir(uploads_dir):
                filepath = os.path.join(uploads_dir, filename)
                if os.path.isfile(filepath):
                    # Delete files older than 1 hour
                    if time.time() - os.path.getmtime(filepath) > 3600:
                        cleanup_file_with_retry(filepath)
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == '__main__':
    # Create uploads directory
    os.makedirs('uploads', exist_ok=True)
    
    # Clean up any old files on startup
    cleanup_old_uploads()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
