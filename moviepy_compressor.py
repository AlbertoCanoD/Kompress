import time
import os
from moviepy.editor import VideoFileClip

def compress_video(video_path, compression_value, update_progress, update_estimates):
    clip = VideoFileClip(video_path)
    output_path = video_path.split(".")[0] + '_compressed.mp4'

    total_frames = clip.reader.nframes  # Obtén el número total de frames
    processed_frames = 0

    start_time = time.time()

    def make_frame(get_frame, t):
        nonlocal processed_frames
        processed_frames += 1

        # Obtén el fotograma actual
        frame = get_frame(t)

        # Estima el progreso y tiempo restante
        elapsed_time = time.time() - start_time

        # Obtener el tamaño actual del archivo comprimido
        if os.path.exists(output_path):
            current_size = os.path.getsize(output_path)
        else:
            current_size = 0  # Si el archivo no existe, el tamaño es 0

        # Estimar el tamaño total basado en el tamaño actual y el número de fotogramas procesados
        estimated_total_size = (current_size / processed_frames) * total_frames if processed_frames > 0 else 0
        remaining_time = (elapsed_time / processed_frames) * (total_frames - processed_frames) if processed_frames > 0 else 0

        # Actualiza las estimaciones
        update_progress(processed_frames, total_frames)
        update_estimates(estimated_total_size, remaining_time)

        return frame

    # Aplicar la función make_frame usando fl_image en lugar de fl, ya que estamos trabajando con imágenes (frames)
    new_clip = clip.fl(lambda gf, t: make_frame(gf, t))
    new_clip = new_clip.resize(height=int(clip.h * compression_value / 100))
    new_clip.write_videofile(output_path, audio_codec='aac')
