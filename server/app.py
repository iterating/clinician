from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
from PIL import Image, ImageDraw
import base64
import io
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuration
IMAGE_MODE = "RGB"
IMAGE_SIZE = (200, 200)
IMAGE_BACKGROUND = "white"
FONT_COLOR = "black"

# CORS Configuration
default_origins = ['https://handwrittenletter.vercel.app']
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',') or default_origins
if os.getenv('FLASK_ENV') == 'development':
    ALLOWED_ORIGINS.extend(['http://localhost:5173', 'http://127.0.0.1:5173'])

CORS_CONFIG = {
    r"/api/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
}

app = Flask(__name__)
CORS(app, resources=CORS_CONFIG)

@app.before_request
def log_request_info():
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())

def create_letter_image(char, size=IMAGE_SIZE):
    """Create a simple letter image"""
    try:
        # Create new image
        img = Image.new(IMAGE_MODE, size, IMAGE_BACKGROUND)
        draw = ImageDraw.Draw(img)
        
        # Draw text at fixed position
        draw.text((size[0]//3, size[1]//3), char, fill=FONT_COLOR)
        
        logger.info(f"Successfully created image for character: {char}")
        return img
    except Exception as e:
        logger.error(f"Error creating letter image: {str(e)}")
        logger.error(traceback.format_exc())
        raise

@app.route('/api/save-letter', methods=['POST'])
def save_letter():
    try:
        logger.info("Starting save_letter endpoint")
        data = request.get_json()
        
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data received'}), 400
            
        letter = data.get('letter', '')
        image_data = data.get('imageData', '')
        
        if not letter or not image_data:
            logger.error("Missing required fields")
            return jsonify({'error': 'Missing letter or image data'}), 400
            
        logger.info(f"Successfully processed letter: {letter}")
        
        # In serverless environment, we'll just acknowledge receipt
        return jsonify({
            'success': True,
            'message': f'Processed letter {letter}'
        })
    except Exception as e:
        logger.error(f"Error in save_letter: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/render', methods=['POST'])
def render_handwriting():
    try:
        logger.info("Starting render_handwriting endpoint")
        data = request.get_json()
        
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data received'}), 400
            
        text = data.get('text', '')
        logger.info(f"Received text: {text}")
        
        # Create image for text
        img = create_letter_image(text[0] if text else 'A')
        logger.info("Image created successfully")
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        logger.info("Image converted to base64")
        
        return jsonify({
            'image': f'data:image/png;base64,{img_str}',
            'text': text
        })
    except Exception as e:
        logger.error(f"Error in render_handwriting: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-test-dataset', methods=['POST'])
def generate_test_dataset():
    try:
        logger.info("Starting generate_test_dataset endpoint")
        data = request.get_json()
        
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data received'}), 400
            
        letterlist = data.get('letterlist', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        logger.info(f"Generating test dataset for letters: {letterlist}")
        
        # Generate a simple test image for 'A'
        img = create_letter_image('A')
        logger.info("Test image created successfully")
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        logger.info("Image converted to base64")
        
        return jsonify({
            'success': True,
            'message': 'Generated test dataset',
            'image': f'data:image/png;base64,{img_str}'
        })
    except Exception as e:
        logger.error(f"Error in generate_test_dataset: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True)
