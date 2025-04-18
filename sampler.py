import tkinter as tk
import pygame
import threading
import time
import os
from tkinter import filedialog

# Configuración
NUM_PADS = 16
NUM_SAMPLES = 4
NUM_STEPS = 16
BPM = 125
STEP_TIME = 60 / BPM / 4
key_bindings = ['z', 'x', 'c', 'v']
sample_paths = ["kick.wav", "clap.wav", "hh.wav", "sample4.wav"]

# Estado
samples = [None] * NUM_PADS
sample_labels = [None] * NUM_PADS
selected_sample_index = 0
current_step = 0
running = False

# Init sonido
pygame.mixer.init()
for i, path in enumerate(sample_paths):
    if os.path.exists(path):
        samples[i] = pygame.mixer.Sound(path)
    else:
        print(f"Archivo no encontrado: {path}")

# Init GUI
root = tk.Tk()
root.title("PO KO Style Step Sequencer")

step_states = [[tk.IntVar() for _ in range(NUM_STEPS)] for _ in range(NUM_PADS)]
volume_vars = [tk.DoubleVar(value=1.0) for _ in range(NUM_PADS)]
write_mode = tk.BooleanVar(value=False)

# Botón Write
def toggle_write():
    if write_mode.get():
        write_mode.set(False)
        render_pad_view()
    else:
        write_mode.set(True)
        render_sequencer_view()

write_button = tk.Button(root, text="Write", command=toggle_write)
write_button.grid(row=0, column=0, sticky="w")

# Frame para la rejilla
pad_grid = tk.Frame(root)
pad_grid.grid(row=1, column=0, columnspan=8, rowspan=4, padx=10, pady=10)

# Vista pads
def select_sample(index):
    global selected_sample_index
    if samples[index]:
        selected_sample_index = index
        samples[index].play()
        update_pad_styles()

def update_pad_styles():
    for i in range(4):
        for j in range(4):
            index = i * 4 + j
            btn = pad_grid.grid_slaves(row=i, column=j)
            if btn:
                if index == selected_sample_index:
                    btn[0].config(bg="#ff9999")
                else:
                    btn[0].config(bg="SystemButtonFace")

def render_pad_view():
    for widget in pad_grid.winfo_children():
        widget.destroy()

    for i in range(4):
        for j in range(4):
            index = i * 4 + j
            sample = samples[index]
            label = os.path.basename(sample_paths[index])[:6] if sample else "(vacío)"
            bg = "#ff9999" if index == selected_sample_index else "SystemButtonFace"
            state = "normal" if sample else "disabled"
            btn = tk.Button(
                pad_grid, text=label, width=8, height=3, bg=bg,
                state=state,
                command=lambda idx=index: select_sample(idx)
            )
            btn.grid(row=i, column=j, padx=2, pady=2)

# Vista secuenciador
def render_sequencer_view():
    for widget in pad_grid.winfo_children():
        widget.destroy()

    for i in range(4):
        for j in range(4):
            step = i * 4 + j
            var = step_states[selected_sample_index][step]
            cb = tk.Checkbutton(pad_grid, variable=var, width=8, height=3)
            cb.grid(row=i, column=j, padx=2, pady=2)

# Cargar sample
def load_sample(index):
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        samples[index] = pygame.mixer.Sound(file_path)
        samples[index].set_volume(volume_vars[index].get())
        sample_labels[index].config(text=os.path.basename(file_path))
        render_pad_view()  # Actualiza etiqueta del pad

# UI de carga y volumen
for row in range(NUM_SAMPLES):
    btn = tk.Button(root, text="Cargar", command=lambda i=row: load_sample(i))
    btn.grid(row=row + 5, column=0)

    label = tk.Label(root, text=os.path.basename(sample_paths[row]) if samples[row] else "Ninguno")
    label.grid(row=row + 5, column=1)
    sample_labels[row] = label

    vol = tk.Scale(root, from_=0.0, to=1.0, resolution=0.01, orient="horizontal",
                   variable=volume_vars[row],
                   command=lambda val, i=row: samples[i].set_volume(float(val)) if samples[i] else None)
    vol.grid(row=row + 5, column=2)

# Secuenciador loop
def sequencer_loop():
    global current_step
    next_time = time.perf_counter()
    while running:
        for sample_index in range(NUM_PADS):
            if step_states[sample_index][current_step].get() == 1:
                if samples[sample_index]:
                    samples[sample_index].play()

        if write_mode.get():
            for i in range(4):
                for j in range(4):
                    step = i * 4 + j
                    widget = pad_grid.grid_slaves(row=i, column=j)
                    if widget:
                        widget[0].config(bg="lime" if step == current_step else "SystemButtonFace")

        next_time += STEP_TIME
        time.sleep(max(0, next_time - time.perf_counter()))
        current_step = (current_step + 1) % NUM_STEPS

# Botón play
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
play_button.grid(row=9, column=0, columnspan=4, sticky="w")

# Teclado
def on_key_press(event):
    key = event.char.lower()
    if key in key_bindings:
        index = key_bindings.index(key)
        if samples[index]:
            samples[index].play()

root.bind("<KeyPress>", on_key_press)

# Iniciar con la vista de pads
render_pad_view()

root.mainloop()
