import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# System Config
CAMERA_ID = os.getenv('CAMERA_ID', '0')
# Convert to int if it's a number, otherwise keep as string (for RTSP URLs)
try:
    CAMERA_ID = int(CAMERA_ID)
except ValueError:
    pass  # Keep as string for video file paths or RTSP URLs

FRAME_WIDTH = int(os.getenv('FRAME_WIDTH', '640'))
FRAME_HEIGHT = int(os.getenv('FRAME_HEIGHT', '640'))
FPS = int(os.getenv('FPS', '30'))

# Model Config
MODEL_PATH = os.getenv('MODEL_PATH', 'yolov8n.pt')
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.5'))

# Validate model path
if not os.path.exists(MODEL_PATH):
    print(f"WARNING: Model file not found at {MODEL_PATH}")
    print("Using default pretrained model. For PPE detection, train a custom model.")
    MODEL_PATH = 'yolov8n.pt'

# Compliance Config
COMPLIANCE_THRESHOLD = float(os.getenv('COMPLIANCE_THRESHOLD', '0.8'))
EVIDENCE_LOCKER_DIR = os.getenv('EVIDENCE_LOCKER_DIR', 
                                os.path.join(os.getcwd(), 'SafeGuardAI', 'evidence_locker'))

# Create evidence locker directory if it doesn't exist
Path(EVIDENCE_LOCKER_DIR).mkdir(parents=True, exist_ok=True)

# Class IDs for Custom YOLO Model
CLASS_IDS = {
    'person': 0,
    'helmet': 1,
    'vest': 2,
    'shoes': 3,  # Added shoes class
    'fire': 4,
    'smoke': 5,
}

# Advanced Hazard Config
SIMULATION_MODE = os.getenv('SIMULATION_MODE', 'False').lower() == 'true'
FALL_RATIO_THRESHOLD = float(os.getenv('FALL_RATIO_THRESHOLD', '1.7'))
VIOLATION_PERSISTENCE_THRESHOLD = int(os.getenv('VIOLATION_PERSISTENCE_THRESHOLD', '10'))
TRACKER_CONFIG = os.getenv('TRACKER_CONFIG', 'bytetrack.yaml')

# Notification Config
NOTIFICATION_RECIPIENTS = os.getenv('NOTIFICATION_RECIPIENTS', 
                                   'manager@company.com,safety_officer@company.com').split(',')

# Logging Config
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'safeguard.log')

