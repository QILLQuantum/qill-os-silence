# qill_os_silence_v0.0.1.py — WITH REAL DRAG-AND-DROP
# (everything from before + module watcher at the end)

# ... [all the previous code you already have] ...

# ——— DRAG-AND-DROP MODULE LOADER ———
import os
import time
from pathlib import Path

MODULES_DIR = Path.home() / "QILL" / "modules"
MODULES_DIR.mkdir(parents=True, exist_ok=True)

loaded_modules = set()

def check_new_modules():
    global loaded_modules
    for pattern_file in MODULES_DIR.glob("*.pattern"):
        if pattern_file.name not in loaded_modules:
            print(f"→ Loading module: {pattern_file.name}")
            loaded_modules.add(pattern_file.name)

def module_watcher():
    while True:
        check_new_modules()
        time.sleep(2)

threading.Thread(target=module_watcher, daemon=True).start()

print(f"Watching {MODULES_DIR}")
print("Drop .pattern files there → magic happens")
# ——————————————————————————————————

plt.show()
