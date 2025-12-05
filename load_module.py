# From main.py — Early Module Loader (watch ~/QILL/modules/)
from pathlib import Path
import time
import threading

MODULES_DIR = Path.home() / "QILL" / "modules"
MODULES_DIR.mkdir(parents=True, exist_ok=True)
loaded = set()

def load_module(pattern_file):
    if pattern_file.name in loaded:
        return
    with open(pattern_file, 'rb') as f:
        data = f.read()
    # Parse header: freq (u16 at offset 64), mode_m/n (u16 at 66/68)
    freq = int.from_bytes(data[64:66], 'little')
    mode_m = int.from_bytes(data[66:68], 'little')
    mode_n = int.from_bytes(data[68:70], 'little')
    print(f"Loaded {pattern_file.name} — Freq: {freq} Hz, Mode: ({mode_m},{mode_n})")
    # Stub: Tweak R2 for superposition
    global R2
    R2 += freq / 10000.0  # Visual ripple
    loaded.add(pattern_file.name)

def watcher():
    while True:
        for f in MODULES_DIR.glob("*.pattern"):
            load_module(f)
        time.sleep(2)

threading.Thread(target=watcher, daemon=True).start()
print(f"Watching {MODULES_DIR}")