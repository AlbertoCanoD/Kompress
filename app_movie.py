# Importing the module
from moviepy.editor import *
import argparse

# Argument parser
parser = argparse.ArgumentParser()
'''required=True,'''
parser.add_argument("-v", "--video", help="video path",
                    default="test_files/test.mp4", type=str)
parser.add_argument("-c", "--compression",
                    help="percent of compression ratio", type=int, default=80)
args = parser.parse_args()

# Exception handling
# If video not found
if args.video is None:
    raise Exception('Video not found, check path')

# Compression check
if args.compression not in range(1, 99):
    raise Exception('Compress percent should be in range 1-99')

# Take video from arguments
video = VideoFileClip(args.video)

# Take compression ratio from arguments
ratio = args.compression / 100

# getting width and height of video 1
width = video.w
height = video.h
print("Width and Height of original video : ", end=" ")
print(str(width) + "px  x ", str(height) + "px")
print("#################################")

# Resize video with gived compression ratio
video_resized = video.resize(ratio)

# getting width and height of video 2 which is resized
width_resized = video_resized.w
height_resized = video_resized.h
print("Width and Height of resized video : ", end=" ")
print(str(width_resized) + "px x ", str(height_resized) + "px")
print("###################################")

# Get name and video extension
video_tuple = args.video.split(".")
video_resized.write_videofile(
    video_tuple[0] + "_compressed.mp4", fps=30)  # TODO// FPS INT ARGS
# TODO // Get original FPS of video, because if we use more fps then video have, it increase the video size

# Only for ipynb
# displaying final clip
# video_resized.ipython_display()
