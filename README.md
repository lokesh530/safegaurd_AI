# SafeGuardAI - Industrial Safety Monitoring System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SafeGuardAI** is an AI-powered safety monitoring system designed for industrial environments. It uses computer vision to detect PPE compliance (helmets, vests, shoes), identify safety hazards (fire, smoke), detect falls, and identify workers using face recognition.

## ⚠️ Current Status

> [!WARNING]
> **This project is currently in development and NOT production-ready.**
> 
> The system requires a properly trained YOLO model with real PPE detection data. The current model was trained on dummy data and cannot detect PPE equipment. See [Dataset Preparation](#dataset-preparation) for next steps.

## Features

- ✅ **PPE Detection**: Monitors workers for helmet, vest, and safety shoe compliance
- ✅ **Fall Detection**: Identifies workers who have fallen based on body orientation
- ✅ **Hazard Detection**: Detects fire and smoke in the monitored area
- ✅ **Worker Identification**: Uses face recognition to identify workers
- ✅ **Violation Tracking**: Persistent violation tracking with configurable thresholds
- ✅ **Alert System**: Sends notifications to managers after sustained violations (60+ seconds)
- ✅ **Evidence Logging**: Captures and stores images of violations
- ✅ **Real-time Dashboard**: Streamlit-based UI for live monitoring
- ✅ **Worker Management**: Registration and onboarding system

## System Requirements

- **Python**: 3.8 or higher
- **OS**: macOS, Linux, or Windows
- **Hardware**: 
  - CPU: Multi-core processor (4+ cores recommended)
  - RAM: 8GB minimum, 16GB recommended
  - GPU: Optional but recommended for better performance (NVIDIA CUDA or Apple Silicon MPS)
  - Camera: USB webcam or IP camera

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SafeGuardAI
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Installing `dlib` and `face_recognition` may require additional system dependencies:

**macOS:**
```bash
brew install cmake
```

**Ubuntu/Debian:**
```bash
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Initialize Database

```bash
python -c "from SafeGuardAI.core.database import init_db; init_db()"
```

## Dataset Preparation

> [!IMPORTANT]
> **Critical Step: The system requires a trained YOLO model with real PPE detection data.**

### Option 1: Download Existing Dataset

**Recommended sources:**
- **Roboflow Universe**: Search for "PPE detection" or "hard hat detection"
  - Example: [Construction Site Safety Dataset](https://universe.roboflow.com/search?q=ppe+detection)
- **Kaggle**: "Construction Site Safety Image Dataset"

### Option 2: Create Custom Dataset

1. **Collect Images**: Record 2-3 hours of video from your target deployment site
2. **Extract Frames**: Use tools like `ffmpeg` to extract frames
3. **Annotate**: Use annotation tools:
   - [Roboflow](https://roboflow.com/) (recommended - cloud-based)
   - [CVAT](https://github.com/opencv/cvat) (self-hosted)
   - [LabelImg](https://github.com/tzutalin/labelImg) (desktop app)

### Dataset Structure

Organize your dataset in YOLO format:

```
dataset/
├── images/
│   ├── train/  (80% of images)
│   └── val/    (20% of images)
├── labels/
│   ├── train/  (corresponding .txt files)
│   └── val/
└── data.yaml
```

**Required classes in `safeguard_data.yaml`:**
```yaml
names:
  0: Person
  1: Helmet
  2: Vest
  3: Fire
  4: Smoke
nc: 5
train: dataset/images/train
val: dataset/images/val
```

**Minimum dataset size**: 3,000+ labeled images for production use

See [docs/DATASET_GUIDE.md](docs/DATASET_GUIDE.md) for detailed instructions.

## Training the Model

Once your dataset is ready:

```bash
python scripts/train.py
```

**Training parameters** (edit in `scripts/train.py`):
- Epochs: 100 (adjust based on dataset size)
- Image size: 640x640
- Batch size: 16 (adjust based on available RAM/GPU)
- Device: 'mps' (Mac), 'cuda' (NVIDIA), or 'cpu'

**Target metrics for production:**
- mAP50-95: >50%
- mAP50: >80%
- Precision: >85%
- Recall: >80%

After training, update `MODEL_PATH` in `.env`:
```env
MODEL_PATH=runs/detect/train/weights/best.pt
```

## Running the Application

### Start the Streamlit Dashboard

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

### Pages

1. **Live Monitor**: Real-time video feed with PPE detection and alerts
2. **Customer Registration**: Register new customers/projects
3. **Worker Management**: Register workers and capture face encodings

## Configuration

All configuration is managed through the `.env` file:

### Camera Settings
```env
CAMERA_ID=0  # 0 for webcam, or path to video file
FRAME_WIDTH=640
FRAME_HEIGHT=640
```

### Model Settings
```env
MODEL_PATH=runs/detect/train/weights/best.pt
CONFIDENCE_THRESHOLD=0.5
```

### Detection Settings
```env
SIMULATION_MODE=False  # Set to True for testing without real model
FALL_RATIO_THRESHOLD=1.7  # Width/Height ratio for fall detection
VIOLATION_PERSISTENCE_THRESHOLD=10  # Frames before flagging violation
```

### Notifications
```env
NOTIFICATION_RECIPIENTS=manager@company.com,safety@company.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Project Structure

```
SafeGuardAI/
├── SafeGuardAI/          # Main package
│   ├── analysis/         # Video processing & detection logic
│   ├── capture/          # Video input handling
│   ├── core/             # Database & metrics
│   ├── ui/               # Streamlit interface
│   └── utils/            # Notification services
├── tests/                # Test files
├── docs/                 # Documentation
├── scripts/              # Training & utility scripts
├── config/               # Configuration files
├── dataset/              # Training data (gitignored)
├── evidence_locker/      # Violation images
├── main.py               # Application entry point
├── config.py             # Configuration loader
└── requirements.txt      # Python dependencies
```

## Troubleshooting

### Import Errors
```bash
# Ensure SafeGuardAI package is in Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/SafeGuardAI"
```

### Camera Not Found
- Check `CAMERA_ID` in `.env`
- Test camera: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`

### Face Recognition Errors
- Ensure `dlib` is properly installed
- On Mac: `brew install cmake` before pip install

### Low FPS
- Reduce `FRAME_WIDTH` and `FRAME_HEIGHT`
- Enable GPU acceleration (CUDA or MPS)
- Increase face recognition interval in `consumer.py`

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Style
```bash
# Format code
black SafeGuardAI/

# Lint
flake8 SafeGuardAI/
```

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment guidelines.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: support@safeguardai.example.com

## Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) for object detection
- [face_recognition](https://github.com/ageitgey/face_recognition) for worker identification
- [Streamlit](https://streamlit.io/) for the web interface
