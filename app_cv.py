import cv2
import sys
import os
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

# File type check
file_extension = args.video.split(".")
if file_extension[1] not in ["mp4", "wav"]:
    raise Exception('Incompatible file type only mp4 or wav required')

# Compression check
if args.compression not in range(1, 100):
    raise Exception('Compress percent should be in range 1-99')


# Resizing all frames to desired percent
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim)


# getting video and then processing it and saving in filename_ouput.mp4
cap = cv2.VideoCapture(args.video)
width = (cap.get(3) * args.compression) / 100
height = (cap.get(4) * args.compression) / 100
# fourcc = cv2.VideoWriter_fourcc(*"MJPG")
out_video = cv2.VideoWriter(
    file_extension[0]+'_compressed.mp4', 0x7634706d, 20.0, (int(width), int(height)), True)
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        frameX = rescale_frame(frame, args.compression)
        out_video.write(frameX)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()

cv2.destroyAllWindows()
