from typing import Final
import cv2
from transformers import CLIPModel, CLIPProcessor
from PIL import Image

from common_types import FrameT, RectCoordsT
from constants import TeamNumber
from trackers.player_tracker import PlayerTrackT
from utils.cache_utils import file_cache


class TeamAssigner:
    MODEL_PATH: Final = "patrickjohncyh/fashion-clip"

    team_classes: tuple[str, str]
    model: CLIPModel
    preprocessor: CLIPProcessor
    team_cache: dict[int, TeamNumber] = {}

    def __init__(self, team_a_class: str, team_b_class: str):
        self.team_classes = (team_a_class, team_b_class)

        self.load_model()

    def load_model(self):
        self.model = CLIPModel.from_pretrained(self.MODEL_PATH)

        preprocessor = CLIPProcessor.from_pretrained(self.MODEL_PATH, use_fast=False)

        if type(preprocessor) is not CLIPProcessor:
            raise TypeError(
                f"Expected preprocessor to be of type CLIPProcessor, got {type(preprocessor)}"
            )

        self.preprocessor = preprocessor

    def get_player_team(self, frame: FrameT, bbox: RectCoordsT):
        image = frame[int(bbox[1]) : int(bbox[3]), int(bbox[0]) : int(bbox[2])]
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)

        inputs = self.preprocessor(
            text=self.team_classes,
            images=pil_image,
            return_tensors="pt",
            padding=True,
        )
        outputs = self.model(**inputs)

        logits_per_image = outputs.logits_per_image
        team_probabilities = logits_per_image.softmax(dim=1)

        result: int = team_probabilities.argmax(dim=1, keepdim=True)[0].item()

        return TeamNumber(result)

    # @file_cache()
    def get_teams(
        self,
        frames: list[FrameT],
        player_tracks: list[PlayerTrackT],
    ):
        self.load_model()

        teams_for_tracks: list[dict[int, TeamNumber]] = []

        for i, track in enumerate(player_tracks):

            if i % 48 == 0:
                self.team_cache.clear()

            teams_for_track: dict[int, TeamNumber] = {}

            for track_id, meta in track.items():
                bbox = meta.get("bbox")
                if bbox is None:
                    continue

                if track_id in self.team_cache:
                    team = self.team_cache[track_id]
                else:
                    team = self.get_player_team(frames[i], bbox)
                    self.team_cache[track_id] = team

                teams_for_track[track_id] = team

            teams_for_tracks.append(teams_for_track)

        return teams_for_tracks
