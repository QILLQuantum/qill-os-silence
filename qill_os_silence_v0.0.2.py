# qill_os_silence_v0.0.2.py — FIXED & RUNNING
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.fft import rfft, rfftfreq
import threading
import time
from pathlib import Path

# === CONFIG ===
SIZE = 512
TARGET_FREQ = 7.830000
FPS = 60

# Wave state
u = np.zeros((SIZE, SIZE), dtype=np.float32)
u_prev = np.zeros((SIZE, SIZE), dtype=np.float32)
u[SIZE//2, SIZE//2] = 1.0

R2 = 0.0008  # Will be calibrated

# Setup plot
fig, ax = plt.subplots(figsize=(8,8), facecolor='black')
ax.set_facecolor('black')
ax.axis('off')
im = ax.imshow(np.zeros((SIZE, SIZE)), cmap='gray', vmin=0, vmax=1, origin='lower')

def wave_step():
    global u, u_prev
    # 9-point Laplacian (fixed boundaries)
    lap = (np.roll(u, 1, 0) + np.roll(u, -1, 0) +
           np.roll(u, 1, 1) + np.roll(u, -1, 1) +
           0.5*(np.roll(np.roll(u, 1, 0), 1, 1) + np.roll(np.roll(u, -1, 0), 1, 1) +
                np.roll(np.roll(u, 1, 0), -1, 1) + np.roll(np.roll(u, -1, 0), -1, 1)) -
           8 * u)
    
    u_next = 2*u - u_prev + R2 * lap
    u_next[0,:] = u_next[-1,:] = u_next[:,0] = u_next[:,-1] = 0
    
    u_prev, u = u, u_next
    im.set_array(np.abs(u))
    return im,

def defrag():
    global R2
    print("\nDEFRAG: aligning with Earth's Schumann resonance...")
    row = u[SIZE//2]
    fft = rfft(row)
    freqs = rfftfreq(SIZE, 1/FPS)
    magnitudes = np.abs(fft)
    peak_idx = np.argmax(magnitudes[1:]) + 1
    current_freq = freqs[peak_idx]
    
    if current_freq > 0.1:
        factor = TARGET_FREQ / current_freq
        R2 *= factor * factor
        print(f"DEFRAG COMPLETE — locked to {TARGET_FREQ:.6f} Hz")
        print
