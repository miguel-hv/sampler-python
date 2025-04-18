import tkinter as tk
import pygame
import threading
import time
import os
from tkinter import filedialog

# Configuración
NUM_SAMPLES = 16
NUM_STEPS = 16
BPM = 125
STEP_TIME = 60 / BPM / 4

key_bindings = ['z', 'x', 'c', 'v']
sample_paths = [None] * NUM_SAMPLES
samples = [None] * NUM_SAMPLES
volume_vars = [1.0] * NUM_SAMPLES
step_states = [[0 for _ in range(NUM_STEPS)] for _ in range(NUM_SAMPLES)]
pad_buttons = [None] * 16

current_step = 0
running = False
write_mode = False
import_mode = False
selected_sample_index = None

pygame.mixer.init()

root = tk.Tk()
root.title("PO KO Style Sequencer")

main_frame = tk.Frame(root)
main_frame.pack()

# Header (Write / Import)
header_frame = tk.Frame(main_frame)
header_frame.grid(row=0, column=0, columnspan=4)

def toggle_write_mode():
    global write_mode, import_mode
    write_mode = not write_mode
    import_mode = False
    import_button.config(relief="raised")
    write_button.config(relief="sunken" if write_mode else "raised")
    render_pad_view()

def toggle_import_mode():
    global import_mode, write_mode
    import_mode = not import_mode
    write_mode = False
    write_button.config(relief="raised")
    import_button.config(relief="sunken" if import_mode else "raised")
    render_pad_view()

write_button = tk.Button(header_frame, text="Write", command=toggle_write_mode)
write_button.pack(side="left", padx=5)

import_button = tk.Button(header_frame, text="Import", command=toggle_import_mode)
import_button.pack(side="left", padx=5)

# Pad grid
pad_grid = tk.Frame(main_frame)
pad_grid.grid(row=1, column=0)

def update_step_state(idx, var):
    if selected_sample_index is not None:
        step_states[selected_sample_index][idx] = var.get()

def update_pad_styles():
    for idx, btn in enumerate(pad_buttons):
        if btn:
            if idx == selected_sample_index:
                btn.config(bg="#ff9999")
            else:
                btn.config(bg="SystemButtonFace")  # O el color que uses por defecto

def on_pad_click(index):
    global selected_sample_index
    selected_sample_index = index
    update_pad_styles()
    if samples[index] and not import_mode and not write_mode:
        samples[index].play()                

def render_pad_view():
    for widget in pad_grid.winfo_children():
        widget.destroy()

    for i in range(4):
        for j in range(4):
            index = i * 4 + j

            if write_mode:
                var = tk.IntVar(value=step_states[selected_sample_index][index] if selected_sample_index is not None else 0)
                cb = tk.Checkbutton(pad_grid, variable=var, command=lambda idx=index, v=var: update_step_state(idx, v))
                cb.grid(row=i, column=j, ipadx=20, ipady=20, padx=2, pady=2)
            elif import_mode:
                if samples[index] is None:
                    btn = tk.Button(pad_grid, text="+", command=lambda idx=index: import_sample(idx), width=6, height=3)
                    btn.grid(row=i, column=j, padx=2, pady=2)
                else:
                    placeholder = tk.Label(pad_grid, text="", width=6, height=3)
                    placeholder.grid(row=i, column=j, padx=2, pady=2)
            else:
                label = os.path.basename(sample_paths[index])[:6] if samples[index] else str(index + 1)

                btn = tk.Button(
                    pad_grid,
                    text=label,
                    width=6,
                    height=3,
                    command=lambda idx=index: on_pad_click(idx)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)

                pad_buttons[index] = btn

    if not write_mode and not import_mode:
        update_pad_styles()
    else:
        pad_buttons[index] = None


def select_sample(index):
    global selected_sample_index
    if not import_mode and samples[index]:
        selected_sample_index = index
        samples[index].play()
        render_pad_view()

def import_sample(index):
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        samples[index] = pygame.mixer.Sound(file_path)
        samples[index].set_volume(volume_vars[index])
        sample_paths[index] = file_path
        render_pad_view()

def sequencer_loop():
    global current_step
    next_time = time.perf_counter()
    while running:
        for sample_index in range(NUM_SAMPLES):
            if step_states[sample_index][current_step] == 1:
                if samples[sample_index]:
                    samples[sample_index].play()

        current_step = (current_step + 1) % NUM_STEPS
        next_time += STEP_TIME
        sleep_time = max(0, next_time - time.perf_counter())
        time.sleep(sleep_time)

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

play_button = tk.Button(main_frame, text="Play", command=toggle_play)
play_button.grid(row=2, column=0, pady=10)

def on_key_press(event):
    key = event.char.lower()
    if key in key_bindings:
        index = key_bindings.index(key)
        if samples[index]:
            samples[index].play()

root.bind("<KeyPress>", on_key_press)

render_pad_view()
root.mainloop()
