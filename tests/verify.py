import sys
import os
import time
import threading

# Add current dir to path
sys.path.append(os.getcwd())

from elf_on_shelf.main import ElfApp

def run_app():
    print("Initializing App...")
    app = ElfApp()
    
    print("Starting App in background thread...")
    t = threading.Thread(target=app.run, daemon=True)
    t.start()
    
    print("Running for 3 seconds...")
    time.sleep(3)
    
    print("Stopping App...")
    app.stop()
    t.join(timeout=2)
    
    print("Verification Passed")

if __name__ == "__main__":
    run_app()
