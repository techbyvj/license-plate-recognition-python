from enum import Enum

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

    class EnvVar:
        PORT = "PORT"

    class DefaultValue:
        DEFAULT_PORT = 5000
