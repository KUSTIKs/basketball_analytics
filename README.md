# Basketball Video Analysis Project

This project analyzes basketball game footage. It uses computer vision to detect and track players and the ball, assign teams based on jersey color, and display this information on the video.

![Preview](./assets/preview.gif)

## 🎯 Core Functionality

- Identifies and tracks players and the ball throughout a video.
- Detects key areas on the basketball court.
- Automatically assigns players to teams based on jersey colors using zero-shot classification.
- Overlays detections, tracks, and team information directly onto video frames for visualization.
- Provides a command-line interface for customizing input/output files and team classification settings.
- Utilizes caching for intermediate results to improve processing speed.

## 📋 Prerequisites

- Python 3.12
- Dependencies as listed in requirements.txt

## ⚙️ Installation

**1. Clone the repository:**

```text
git clone <repo-link>
cd <repo-directory>
```

**2. Set up a virtual environment (recommended):**

```text
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**

```text
pip install -r requirements.txt
```

## 🧠 Models

The project uses pre-trained models for detecting the ball (`models/ball_detector.pt`), court keypoints (`models/court_keypoint_detector.pt`), and players (`models/player_detector.pt`). These models are downloaded automatically from the Hugging Face during the first run if they aren't already in the `models/` directory. An internet connection is needed for this initial download.

## 🚀 Usage

Run the analysis using the `main.py` script from your terminal.

**Basic execution (uses default video and settings):**

```bash
python main.py path/to/your/input_video.mp4
```

**Specify input and output files:**

```bash
python main.py your_input_video.mp4 --output-video processed_game.avi
```

**Customize team jersey descriptions:**

```bash
python main.py your_input_video.mp4 --output-video output.avi --team-a-class "Players in red jerseys" --team-b-class "Players in light yellow jerseys"
```

### Command-Line Arguments

- `input_video`: Path to the input video. Defaults to the value in `constants.INPUT_VIDEO`.
- `--output-video`: Path for the saved output video. Defaults to `constants.OUTPUT_VIDEO`.
- `--team-a-class`: Jersey description for Team A. Default: "Dark blue shirt".
- `--team-b-class`: Jersey description for Team B. Default: "White shirt".

## 🧪 Running Tests

This project includes unit tests using `pytest`. To run them, navigate to the project's root directory in your terminal and execute:

```bash
pytest
```

This will automatically discover and run all tests located in the tests/ directory.

## 🛠️ Key Libraries & Frameworks

- Ultralytics (YOLO)
- OpenCV
- NumPy
- PyTorch

## 📁 Project Structure

```text
.
├── assets/                 # Static assets (e.g., court images)
├── drawers/                # Modules for drawing visualizations
├── input_videos/           # Directory for input videos
├── models/                 # Pre-trained models (auto-downloaded)
├── tests/                  # Unit tests for the project
│   └── test_*.py           # Individual test files
├── trackers/               # Modules for object tracking & game events
├── utils/                  # Utility scripts (caching, geometry, etc.)
├── common_types.py         # Common type definitions
├── constants.py            # Project-wide constants
├── main.py                 # Main script for the analysis pipeline
└── requirements.txt        # Project dependencies
```

## 📄 Sources & Citations

This project was developed as part of the BI-PYT course.

**Tutorial Inspiration:** Inspired by the ["Build an AI/ML NBA Basketball Analysis system with YOLO, OpenCV, and Python"](https://www.youtube.com/watch?v=QqVahw9tBfw&ab_channel=CodeInaJiffy) tutorial by Code In a Jiffy.
