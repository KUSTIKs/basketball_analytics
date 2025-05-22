from typing import Final

from utils.video_utils import read_video, save_video

input_video_path: Final = "./input_videos/video_1.mp4"
output_video_path: Final = "./output_videos/video.avi"


def main():
    video_frames = read_video(input_video_path)

    save_video(video_frames, output_video_path)


if __name__ == "__main__":
    main()
