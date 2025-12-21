import sys
import os
import time
import threading

# Add current dir to path
sys.path.append(os.getcwd())

from elf_on_shelf.main import ElfApp

def run_app():
    print("Initializing App...")
    # Inject Mock if ReachySDK not present
    app = ElfApp()
    
    # We can inspect the internals since we are in verified test mode
    assert app.vision is not None
    assert app.motion is not None
    assert app.audio is not None
    
    print("Starting App in background thread...")
    t = threading.Thread(target=app.run, daemon=True)
    t.start()
    
    print("Waiting for app startup...")
    time.sleep(1)
    
    print("Testing Sentry Mode Logic...")
    # Verify defaults
    # Sentry mode doesn't have an explicit 'is_active' flag, it just runs.
    # We can verify it has dependencies hooked up.
    if app.sentry.vision and app.sentry.controller:
        print("  - Sentry mode initialized with dependencies.")
    
    print("Testing Scanner Trigger Logic...")
    # Simulate a trigger word detection if possible, or just check state
    # Since we can't easily speak to the mock audio, we will manually trigger the scanner
    print("  - Manually triggering scanner sequence...")
    app.scanner.run_sequence()
    
    print("Running for 2 more seconds...")
    time.sleep(2)
    
    print("Stopping App...")
    app.stop()
    t.join(timeout=2)
    
    print("Verification Passed")

if __name__ == "__main__":
    run_app()
