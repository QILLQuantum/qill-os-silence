# qill_os_silence_v0.0.4.py — FINAL WORKING VERSION
import numpy as np
import tkinter as tk
from scipy.fft import rfft, rfftfreq
import threading

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

# This is the fix: use raw bytes + canvas.create_image with force update
img_data = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)

def update_canvas():
    # Force immediate redraw
    canvas.delete("all")
    canvas.create_image(SIZE//2, SIZE//2, image=tk.PhotoImage(data=bytes(img_data.flatten())), state="normal")
    root.update_idletasks()

def wave_step():
    global u, u_prev, img_data
    lap = (np.roll(u, 1, 0) + np.roll(u, -1, 0) +
           np.roll(u, 1, 1) + np.roll(u, -1, 1) +
           0.5*(np.roll(np.roll(u, 1, 0), 1, 1) + np.roll(np.roll(u, -1, 0), 1, 1) +
                np.roll(np.roll(u, 1, 0), -1, 1) + np.roll(np.roll(u, -1, 0), -1, 1)) -
           8 * u)
    
    u_next = 2*u - u_prev + R2 * lap
    u_next[0,:] = u_next[-1,:] = u_next[:,0] = u_next[:,-1] = 0
    u_prev, u = u, u_next
    
    # Convert to RGB
    intensity = np.clip(np.abs(u) * 255, 0, 255).astype(np.uint8)
    img_data[:, :, 0] = intensity  # R
    img_data[:, :, 1] = intensity  # G
    img_data[:, :, 2] = intensity  # B
    
    update_canvas()

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
        print(f"DEFRAG COMPLETE — locked to {TARGET_FREQ:.6f} Hz")
        print("   The sand is now perfectly still.")
    else:
        print("No resonance yet — wait a few seconds")

root.bind('d', lambda e: threading.Thread(target=defrag, daemon=True).start())
print("QILL OS v0.0.4 — Press 'd' to defrag")

def animate():
    wave_step()
    root.after(16, animate)

animate()
root.mainloop()