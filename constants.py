from enum import Enum
import os
from typing import Final


INPUT_VIDEO: Final = "./input_videos/video_1.mp4"
OUTPUT_VIDEO: Final = "./output_videos/video.avi"

MODELS_DIR: Final = "./models"

PLAYER_MODEL: Final = os.path.join(MODELS_DIR, "player_detector.pt")
BALL_MODEL: Final = os.path.join(MODELS_DIR, "ball_detector.pt")
COURT_KEYPOINT_MODEL: Final = os.path.join(MODELS_DIR, "court_keypoint_detector.pt")

CACHE_DIR: Final = "./cache"

COURT_IMAGE_PATH: Final = "./assets/basketball_court.png"


class YOLOClassName(str, Enum):
    PLAYER = "Player"
    BALL = "Ball"


class TeamNumber(int, Enum):
    A = 0
    B = 1
