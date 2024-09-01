import cv2
import os
import time

def compress_video(video_path, compression_value, update_progress, update_estimates):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(3) * compression_value / 100)
    height = int(cap.get(4) * compression_value / 100)
    output_path = video_path.split(".")[0] + '_compressed.mp4'

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total de frames en el video
    processed_frames = 0

    start_time = time.time()
    initial_size = os.path.getsize(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_resized = cv2.resize(frame, (width, height))
            out_video.write(frame_resized)

            # Actualiza el progreso
            processed_frames += 1
            update_progress(processed_frames, total_frames)

            # Estimación del tiempo restante y tamaño comprimido
            elapsed_time = time.time() - start_time
            current_size = os.path.getsize(output_path)
            estimated_total_size = (current_size / processed_frames) * total_frames
            remaining_time = (elapsed_time / processed_frames) * (total_frames - processed_frames)

            # Actualiza las estimaciones en la interfaz
            update_estimates(estimated_total_size, remaining_time)

        else:
            break

    cap.release()
    out_video.release()
