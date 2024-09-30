import pytesseract
import easyocr
import logging
import os
import time
from datetime import datetime
import cv2
import numpy as np


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define what can be imported from this module
__all__ = ['process_license_plate']

def process_license_plate(image):
    license_plate = detect_license_plate(image)
    if license_plate is None:
        logging.warning("No license plate detected")
        return None, None
    
    text = recognize_text(license_plate)
    
    # Create output folder and save images
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_folder = os.path.join("output", current_date)
    os.makedirs(output_folder, exist_ok=True)
    
    # Save original image
    original_filename = f"original_{int(time.time())}.jpg"
    original_path = os.path.join(output_folder, original_filename)
    cv2.imwrite(original_path, image)
    logging.info(f"Original image saved as {original_path}")
    
    # Save license plate image
    if text and text != "unknown":
        sanitized_text = ''.join(c for c in text if c.isalnum())
        plate_filename = f"plate_{sanitized_text}_{int(time.time())}.jpg"
    else:
        plate_filename = f"plate_unrecognized_{int(time.time())}.jpg"
    plate_path = os.path.join(output_folder, plate_filename)
    cv2.imwrite(plate_path, license_plate)
    logging.info(f"License plate image saved as {plate_path}")
    
    if text:
        logging.info(f"Detected license plate text: {text}")
    else:
        logging.warning("No text detected on the license plate")
        text = "unknown"
    
    return license_plate, text

def detect_license_plate(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create yellow and white masks
    lower_yellow = np.array([10, 50, 50])
    upper_yellow = np.array([40, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    
    # Combine masks and apply morphological operations
    combined_mask = cv2.bitwise_or(yellow_mask, white_mask)
    kernel = np.ones((5,5), np.uint8)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    
    # Find and sort contours
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    # Find license plate contour
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if 4 <= len(approx) <= 8:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            area = cv2.contourArea(contour)
            if 1.0 <= aspect_ratio <= 6.0 and area > 500:
                return image[y:y+h, x:x+w]
    
    return None

def recognize_text(image):
    # Try Tesseract OCR first
    config = '--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(image, config=config).strip()
    
    if text:
        logging.info(f"Text recognized by Tesseract OCR: {text}")
        return text
    
    # If Tesseract fails, try EasyOCR
    logging.info("Tesseract OCR failed to recognize text, switching to EasyOCR")
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)
    text = ''.join([result[1] for result in results])
    
    if text:
        logging.info(f"Text recognized by EasyOCR: {text}")
    else:
        logging.warning("Both Tesseract and EasyOCR failed to recognize text")
    
    return text.strip()


