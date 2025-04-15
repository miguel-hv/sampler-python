import tkinter as tk
import pygame
import threading
import time
import os
from tkinter import filedialog


# Configuración
NUM_SAMPLES = 4
NUM_STEPS = 16
BPM = 125
STEP_TIME = 60 / BPM / 4  # tiempo por paso (a semicorcheas)

sample_paths = ["kick.wav", "clap.wav", "hh.wav", "sample4.wav"]
samples = [None] * NUM_SAMPLES
sample_labels = [None] * NUM_SAMPLES
step_states = [[None for _ in range(NUM_STEPS)] for _ in range(NUM_SAMPLES)]
current_step = 0
running = False

# Cargar sonidos
pygame.mixer.init()
for i, path in enumerate(sample_paths):
    if os.path.exists(path):
        samples[i] = pygame.mixer.Sound(path)
    else:
        print(f"Archivo no encontrado: {path}")

# GUI
root = tk.Tk()
root.title("PO KO Step Sequencer")

# Crear botones (checkboxes)
def load_sample(index):
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        samples[index] = pygame.mixer.Sound(file_path)
        sample_labels[index].config(text=os.path.basename(file_path))

for row in range(NUM_SAMPLES):
    # Botón para cargar sample
    btn = tk.Button(root, text="Cargar", command=lambda i=row: load_sample(i))
    btn.grid(row=row, column=0)

    # Etiqueta con el nombre del archivo
    label = tk.Label(root, text=os.path.basename(sample_paths[row]) if samples[row] else "Ninguno")
    label.grid(row=row, column=1)
    sample_labels[row] = label

    # Checkboxes del secuenciador
    for col in range(NUM_STEPS):
        var = tk.IntVar()
        step_states[row][col] = var
        cb = tk.Checkbutton(root, variable=var)
        cb.grid(row=row, column=col + 2)


# Indicación visual de paso actual
step_labels = [tk.Label(root, text=" ") for _ in range(NUM_STEPS)]
for col, label in enumerate(step_labels):
    label.grid(row=NUM_SAMPLES, column=col)

# Loop del secuenciador (en un hilo)
def sequencer_loop():
    global current_step
    next_time = time.perf_counter()
    while running:
        # Toca los sonidos activos
        for sample_index in range(NUM_SAMPLES):
            if step_states[sample_index][current_step].get() == 1:
                if samples[sample_index]:
                    samples[sample_index].play()

        # Indicar visualmente el paso
        for i, label in enumerate(step_labels):
            label.config(text=">" if i == current_step else " ")

        # Espera al próximo paso
        next_time += STEP_TIME
        sleep_time = max(0, next_time - time.perf_counter())
        time.sleep(sleep_time)

        current_step = (current_step + 1) % NUM_STEPS

# Botón Start/Stop
def toggle_play():
    global running, current_step
    if not running:
        running = True
        current_step = 0
        threading.Thread(target=sequencer_loop, daemon=True).start()
        play_button.config(text="Stop")
    else:
        running = False
        play_button.config(text="Play")

play_button = tk.Button(root, text="Play", command=toggle_play)
play_button.grid(row=NUM_SAMPLES + 1, column=0, columnspan=4, sticky="w")

root.mainloop()
