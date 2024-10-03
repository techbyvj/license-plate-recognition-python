from flask import Flask, request, jsonify
import cv2
import numpy as np
import logging
from dotenv import load_dotenv
import os
from constants import ErrorCode, Constants
from plate_recognize_py import process_license_plate

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

class LicensePlateError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

def validate_file_request():
    if 'file' not in request.files:
        logger.warning("No file part in the request")
        raise LicensePlateError(Constants.ErrorMessage.NO_FILE, ErrorCode.NO_FILE)
    
    file = request.files['file']
    if file.filename == '':
        logger.warning("No selected file")
        raise LicensePlateError(Constants.ErrorMessage.NO_SELECTED_FILE, ErrorCode.NO_SELECTED_FILE)
    
    return file

def read_image_file(file):
    logger.info(f"Processing file: {file.filename}")
    return cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

def process_license_plate_image(image):
    config = {
        'save_output': True,
        'output_dir': 'output'
    }
    license_plate, text = process_license_plate(image, config)
    if license_plate is None or text is None:
        logger.warning("No license plate detected or text recognized")
        raise LicensePlateError(Constants.ErrorMessage.NO_PLATE_DETECTED, ErrorCode.NO_PLATE_DETECTED)
    logger.info(f"Successfully processed license plate. Text: {text}")
    return text

@app.route('/process_image', methods=['POST'])
def process_image_api():
    try:
        logger.info("Received image processing request")
        file = validate_file_request()
        image = read_image_file(file)
        text = process_license_plate_image(image)
        return jsonify({"text": text})
    except LicensePlateError as e:
        logger.error(f"License plate error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e), "error_code": e.error_code.value}), 400
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        return jsonify({"error": Constants.ErrorMessage.PROCESSING_ERROR, "error_code": ErrorCode.PROCESSING_ERROR.value}), 500

if __name__ == "__main__":
    logger.info("Starting the Flask application")
    port = int(os.getenv(Constants.EnvVar.PORT, Constants.DefaultValue.DEFAULT_PORT))
    app.run(host="0.0.0.0", port=port, debug=True)

