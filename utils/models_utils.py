import os
import urllib.request

from constants import MODELS_DIR

MODEL_URLS = {
    "player_detector.pt": "https://huggingface.co/kustiks/basketball_analyzer_bi_pyt/resolve/main/player_detector.pt",
    "ball_detector.pt": "https://huggingface.co/kustiks/basketball_analyzer_bi_pyt/resolve/main/ball_detector.pt",
    "court_keypoint_detector.pt": "https://huggingface.co/kustiks/basketball_analyzer_bi_pyt/resolve/main/court_keypoint_detector.pt",
}


def download_models():
    for filename, url in MODEL_URLS.items():
        os.makedirs(MODELS_DIR, exist_ok=True)
        path = os.path.join(MODELS_DIR, filename)

        if not os.path.exists(path):
            print(f"Downloading {filename} model from {url}...")
            urllib.request.urlretrieve(url, path)
            print(f"Downloaded {filename} and saved to {path}")
        else:
            print(f"Using existing local model: {filename}")

    print()
