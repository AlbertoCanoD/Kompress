import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
import threading

import ffmpeg_compressor
import moviepy_compressor
import opencv_compressor


def select_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.wav")])
    if file_path:
        video_path.set(file_path)
        update_video_info()


def update_video_info():
    if video_path.get():
        video_size = os.path.getsize(video_path.get()) / (1024 * 1024)  # Tamaño en MB
        original_size.set(f"Tamaño original: {video_size:.2f} MB")
        compressed_size.set("Tamaño comprimido: N/A")
        time_remaining.set("Tiempo restante: N/A")


def compress_video():
    # Inicia un hilo separado para la compresión de video
    compression_thread = threading.Thread(target=perform_compression)
    compression_thread.start()


def perform_compression():
    if not video_path.get():
        messagebox.showerror("Error", "Por favor, selecciona un video.")
        return

    compression_value = compression_scale.get()
    method = compression_method.get()
    start_time = time.time()

    if method == "OpenCV":
        opencv_compressor.compress_video(video_path.get(), compression_value, update_progress, update_estimates)
    elif method == "FFMPEG":
        ffmpeg_compressor.compress_video(video_path.get(), compression_value)
    elif method == "MoviePy":
        moviepy_compressor.compress_video(video_path.get(), compression_value, update_progress, update_estimates)
    else:
        messagebox.showerror("Error", "Método de compresión no válido.")
        return

    output_path = os.path.splitext(video_path.get())[0] + '_compressed.mp4'
    compressed_video_size = os.path.getsize(output_path) / (1024 * 1024)
    compressed_size.set(f"Tamaño comprimido: {compressed_video_size:.2f} MB")
    end_time = time.time()
    elapsed_time = end_time - start_time
    messagebox.showinfo("Tiempo de Conversión", f"Tiempo total: {elapsed_time:.2f} segundos")


def update_progress(value, max_value):
    progress_percent = int((value / max_value) * 100)  # Calcula el porcentaje sin decimales
    progress.set(progress_percent)
    progress_label.config(text=f"{progress_percent}%")  # Actualiza la etiqueta con el porcentaje
    root.update_idletasks()  # Asegura que la interfaz se actualice


def update_estimates(estimated_size, remaining_time):
    compressed_size.set(f"Tamaño estimado: {estimated_size / (1024 * 1024):.2f} MB")
    time_remaining.set(f"Tiempo restante: {remaining_time:.2f} segundos")
    root.update_idletasks()  # Asegura que la interfaz se actualice


def update_label(value):
    percentage_label.config(text=f"{value}%")


# Configuración de la ventana principal
root = ThemedTk(theme="breeze")
root.title("Kompress - Compresor de Videos")

# Cargar y establecer el logo como ícono
logo_img = Image.open("kompress_logo.png")
logo_photo = ImageTk.PhotoImage(logo_img)
root.iconphoto(False, logo_photo)

# Variables y configuración de estilos
video_path = tk.StringVar()
original_size = tk.StringVar()
compressed_size = tk.StringVar()
time_remaining = tk.StringVar()
compression_method = tk.StringVar(value="OpenCV")
progress = tk.DoubleVar()
compression_value = tk.IntVar()

# Creación de los elementos de la interfaz
ttk.Label(root, text="Seleccione un video:").pack(pady=10)
ttk.Entry(root, textvariable=video_path, width=50).pack(padx=10)
ttk.Button(root, text="Buscar", command=select_video).pack(pady=5)

ttk.Label(root, textvariable=original_size).pack(pady=10)
ttk.Label(root, textvariable=compressed_size).pack(pady=5)
ttk.Label(root, textvariable=time_remaining).pack(pady=5)

# Frame para la barra de compresión y la etiqueta del porcentaje
scale_frame = ttk.Frame(root)
scale_frame.pack(pady=10)

ttk.Label(scale_frame, text="Seleccione porcentaje de compresión:").pack(side=tk.LEFT)
compression_scale = ttk.Scale(scale_frame, from_=1, to=99, orient="horizontal", variable=compression_value,
                              command=lambda x: update_label(int(float(x))))
compression_scale.set(80)
compression_scale.pack(side=tk.LEFT)

percentage_label = ttk.Label(scale_frame, text="80%")
percentage_label.pack(side=tk.LEFT, padx=10)

ttk.Label(root, text="Seleccione el método de compresión:").pack(pady=10)
ttk.Radiobutton(root, text="OpenCV", variable=compression_method, value="OpenCV").pack(anchor=tk.W)
ttk.Radiobutton(root, text="FFMPEG", variable=compression_method, value="FFMPEG").pack(anchor=tk.W)
ttk.Radiobutton(root, text="MoviePy", variable=compression_method, value="MoviePy").pack(anchor=tk.W)

# Barra de progreso y etiqueta para mostrar el porcentaje
progress_frame = ttk.Frame(root)
progress_frame.pack(pady=20, fill=tk.X, padx=10)

progressbar = ttk.Progressbar(progress_frame, variable=progress, maximum=100)
progressbar.pack(side=tk.LEFT, fill=tk.X, expand=True)

progress_label = ttk.Label(progress_frame, text="0%")
progress_label.pack(side=tk.LEFT, padx=10)

ttk.Button(root, text="Comprimir Video", command=compress_video).pack(pady=20)

# Inicialización de la interfaz
update_video_info()
root.mainloop()
