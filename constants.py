from enum import Enum
from typing import Final


INPUT_VIDEO: Final = "./input_videos/video_3.mp4"
OUTPUT_VIDEO: Final = "./output_videos/video.avi"

PLAYER_MODEL: Final = "./models/player_detector.pt"
BALL_MODEL: Final = "./models/ball_detector.pt"
COURT_KEYPOINT_MODEL: Final = "./models/court_keypoint_detector.pt"

CACHE_DIR: Final = "./cache"

COURT_IMAGE_PATH: Final = "./assets/basketball_court.png"


class YOLOClassName(str, Enum):
    PLAYER = "Player"
    BALL = "Ball"


class TeamNumber(int, Enum):
    A = 0
    B = 1
