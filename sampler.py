import pygame
import tkinter as tk
from tkinter import filedialog

# Iniciar Pygame
pygame.init()
pygame.mixer.init()

# Ventana principal
root = tk.Tk()
root.title("Mini Sampler")
root.geometry("400x300")

# Variables
NUM_SAMPLES = 4
sounds = [None] * NUM_SAMPLES
labels = ["Empty"] * NUM_SAMPLES
buttons = []
keys = ['z', 'x', 'c', 'v']

def load_sound(index):
    filepath = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.ogg *.mp3")])
    if filepath:
        sounds[index] = pygame.mixer.Sound(filepath)
        labels[index] = filepath.split("/")[-1]  # Solo el nombre del archivo
        buttons[index]["text"] = f"{keys[index].upper()}: {labels[index]}"

def play_sound(index):
    if sounds[index]:
        sounds[index].play()

# Crear botones
for i in range(NUM_SAMPLES):
    btn = tk.Button(root, text=f"{keys[i].upper()}: {labels[i]}", width=30, height=2,
                    command=lambda i=i: play_sound(i))
    btn.grid(row=i, column=0, padx=10, pady=5)
    buttons.append(btn)

# Botones para cargar sonidos
for i in range(NUM_SAMPLES):
    load_btn = tk.Button(root, text="Cargar", command=lambda i=i: load_sound(i))
    load_btn.grid(row=i, column=1, padx=5)

# Manejo de teclado
def on_key(event):
    key = event.char.lower()
    if key in keys:
        index = keys.index(key)
        play_sound(index)

root.bind("<Key>", on_key)

# Iniciar loop de la interfaz
root.mainloop()
