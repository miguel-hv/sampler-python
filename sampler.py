import tkinter as tk
from tkinter import filedialog
import pygame

# Inicializar pygame mixer
pygame.mixer.init()

# Ventana principal
root = tk.Tk()
root.title("Mini Sampler")

# Lista para guardar los sonidos cargados
samples = [None] * 4  # 4 pads

def cargar_sample(idx):
    filepath = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if filepath:
        samples[idx] = pygame.mixer.Sound(filepath)

def reproducir_sample(idx):
    if samples[idx]:
        samples[idx].play()

# Crear 4 botones de carga y reproducción
for i in range(4):
    frame = tk.Frame(root)
    frame.pack(pady=5)

    cargar_btn = tk.Button(frame, text=f"Cargar Sample {i+1}", command=lambda i=i: cargar_sample(i))
    cargar_btn.pack(side="left", padx=5)

    play_btn = tk.Button(frame, text=f"Play {i+1}", command=lambda i=i: reproducir_sample(i))
    play_btn.pack(side="right", padx=5)

root.mainloop()
