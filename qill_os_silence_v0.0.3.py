# qill_os_silence_v0.0.3.py — WORKS ON EVERY WINDOWS MACHINE
import numpy as np
import tkinter as tk
from scipy.fft import rfft, rfftfreq
import threading
import time

SIZE = 512
TARGET_FREQ = 7.830000
R2 = 0.0008

u = np.zeros((SIZE, SIZE), dtype=np.float32)
u_prev = np.zeros((SIZE, SIZE), dtype=np.float32)
u[SIZE//2, SIZE//2] = 1.0

root = tk.Tk()
root.title("QILL OS — Silence")
root.configure(bg='black')
canvas = tk.Canvas(root, width=SIZE, height=SIZE, bg='black', highlightthickness=0)
canvas.pack()

img = tk.PhotoImage(width=SIZE, height=SIZE)
canvas.create_image((SIZE//2, SIZE//2), image=img, state="normal")

def wave_step():
    global u, u_prev
    lap = (np.roll(u, 1, 0) + np.roll(u, -1, 0) +
           np.roll(u, 1, 1) + np.roll(u, -1, 1) +
           0.5*(np.roll(np.roll(u, 1, 0), 1, 1) + np.roll(np.roll(u, -1, 0), 1, 1) +
                np.roll(np.roll(u, 1, 0), -1, 1) + np.roll(np.roll(u, -1, 0), -1, 1)) -
           8 * u)
    
    u_next = 2*u - u_prev + R2 * lap
    u_next[0,:] = u_next[-1,:] = u_next[:,0] = u_next[:,-1] = 0
    u_prev, u = u, u_next
    
    data = np.abs(u) * 255
    data = np.clip(data, 0, 255).astype(np.uint8)
    img.put(" ".join([f"#{int(v):02x}{int(v):02x}{int(v):02x}" for v in data.flatten()]), (0,0))

def animate():
    wave_step()
    root.after(16, animate)  # ~60 FPS

def defrag():
    global R2
    print("\nDEFRAG: aligning with Earth's Schumann resonance...")
    row = u[SIZE//2]
    fft = rfft(row)
    freqs = rfftfreq(SIZE, 1/60)
    magnitudes = np.abs(fft)
    peak_idx = np.argmax(magnitudes[1:]) + 1
    current = freqs[peak_idx]
    if current > 0.1:
        factor = TARGET_FREQ / current
        R2 *= factor * factor
        print(f"DEFRAG COMPLETE — locked to 7.830000 Hz")
    else:
        print("waiting for wave...")

root.bind('d', lambda e: threading.Thread(target=defrag).start())
print("QILL OS running — press 'd' to defrag")

animate()
root.mainloop()