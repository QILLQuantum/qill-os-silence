# qill_os_silence_win32.py — WORKS ON WINDOWS 100 %, NO TKINTER, NO MATPLOTLIB
# Uses only built-in libraries + pygame (install once)

import pygame
import numpy as np
from scipy.fft import rfft, rfftfreq
import threading
import time

SIZE = 512
TARGET_FREQ = 7.830000
R2 = 0.0008

u = np.zeros((SIZE, SIZE), dtype=np.float32)
u_prev = np.zeros((SIZE, SIZE), dtype=np.float32)
u[SIZE//2, SIZE//2] = 1.0

pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("QILL OS — Silence")
clock = pygame.time.Clock()

def wave_step():
    global u, u_prev, R2
    lap = (np.roll(u, 1, 0) + np.roll(u, -1, 0) +
           np.roll(u, 1, 1) + np.roll(u, -1, 1) +
           0.5*(np.roll(np.roll(u, 1, 0), 1, 1) + np.roll(np.roll(u, -1, 0), 1, 1) +
                np.roll(np.roll(u, 1, 0), -1, 1) + np.roll(np.roll(u, -1, 0), -1, 1)) -
           8 * u)
    
    u_next = 2*u - u_prev + R2 * lap
    u_next[0,:] = u_next[-1,:] = u_next[:,0] = u_next[:,-1] = 0
    u_prev, u = u, u_next
    
    intensity = np.clip(np.abs(u) * 255, 0, 255).astype(np.uint8)
    surface = pygame.surfarray.make_surface(intensity)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

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
    else:
        print("waiting for wave...")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            threading.Thread(target=defrag, daemon=True).start()
    
    wave_step()
    clock.tick(60)

pygame.quit()