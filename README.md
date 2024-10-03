# License Plate Recognition API

This project provides a Flask-based API for license plate recognition using computer vision techniques and OCR (Optical Character Recognition).

## Features

- License plate detection from images
- Text recognition from detected license plates
- Support for both Tesseract OCR and EasyOCR
- Error handling and logging
- Configurable through environment variables
- Image preprocessing and enhancement
- Supports various image formats
- Saves processed license plate images

## Prerequisites

- Python 3.8+
- pip
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract#installing-tesseract) installed on your system

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/techbyvj/license-plate-recognition-python.git
   cd license-plate-recognition-api
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   PORT=5000
   ```

## Usage

To start the API server, run:

```
python main.py
```

The API will be available at `http://localhost:5000` (or the port you specified in the .env file).

### API Endpoints

1. License Plate Recognition
   - URL: `/process_image`
   - Method: POST
   - Body: Form-data with key 'file' and value as the image file
   - Response: JSON object containing the recognized license plate text

Example using curl:
```
curl -X POST -F "file=@path/to/your/image.jpg" http://localhost:5000/process_image
```

## Error Handling

The API uses custom error codes and messages for different scenarios. These are defined in the `constants.py` file:

```python
class ErrorCode(Enum):
    NO_FILE = 1001
    NO_SELECTED_FILE = 1002
    NO_PLATE_DETECTED = 1003
    PROCESSING_ERROR = 1004

class Constants:
    class ErrorMessage:
        NO_FILE = "No file part in the request"
        NO_SELECTED_FILE = "No selected file"
        NO_PLATE_DETECTED = "No license plate detected or text recognized"
        PROCESSING_ERROR = "Error processing image"
```

## Image Processing

The image processing pipeline includes the following steps:

1. Convert the image to HSV color space
2. Create yellow and white masks to isolate potential license plate regions
3. Apply morphological operations to reduce noise
4. Find and analyze contours to detect the license plate
5. Use OCR (Tesseract and EasyOCR) to recognize text on the license plate

## For More Details

For more detailed information about the implementation, usage, and additional features, please visit the project's GitHub repository:

[https://github.com/techbyvj/PlateRecognizePy](https://github.com/techbyvj/PlateRecognizePy)

This repository contains the full source code, documentation, and examples to help you get started with the License Plate Recognition API.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Connect with the Author

Follow the author on X (Twitter): [@saidbyvj](https://x.com/saidbyvj)
