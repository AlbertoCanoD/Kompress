import subprocess

def compress_video(video_path, compression_value):
    output_path = video_path.split(".")[0] + '_compressed.mp4'
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"scale=iw*{compression_value}/100:ih*{compression_value}/100",
        '-c:a', 'copy',  # Copiar el audio sin recodificar
        output_path
    ]
    subprocess.run(command)
