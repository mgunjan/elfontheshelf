import time
import logging
import threading
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ValidateScanner")

def mock_audio_trigger(app):
    """Wait 5 seconds then simulate a Loud Noise (Trigger)."""
    time.sleep(5)
    logger.info("💥 SIMULATING LOUD CLAP (Energy Spike)...")
    app.audio.triggered = True

if __name__ == "__main__":
    # Ensure dependencies
    try:
        import sounddevice
        import numpy
    except ImportError:
        logger.error("Missing sounddevice or numpy. Cannot validate Local Scanner.")
        sys.exit(1)

    logger.info("Initializing App for Scanner Validation...")
    
    # Mock ReachyMini to avoid imports if not needed, or use the real MockReachy from main
    # We will import the real app to test the real logic
    try:
        from elf_on_shelf.main import ElfApp
    except ImportError as e:
         logger.error(f"Import failed: {e}")
         sys.exit(1)

    # Run app in thread
    app = ElfApp(host='localhost')
    
    # Override magic mode so it doesn't get in the way of logs?
    # No, we want to see integration.
    
    logger.info("Starting App Background Thread...")
    app_thread = threading.Thread(target=app.run, daemon=True)
    app_thread.start()

    # Start trigger simulator
    trigger_thread = threading.Thread(target=mock_audio_trigger, args=(app,), daemon=True)
    trigger_thread.start()
    
    # Monitor for 15 seconds
    logger.info("Monitoring for 15 seconds...")
    start_time = time.time()
    scanner_verified = False
    
    try:
        while time.time() - start_time < 15:
            if app.scanner.is_active:
                logger.info("✅ Scanner State: ACTIVE")
                scanner_verified = True
            time.sleep(0.5)
            
        if scanner_verified:
            logger.info("✅ SUCCESS: Scanner activated upon trigger.")
        else:
            logger.error("❌ FAILURE: Scanner did not activate.")
            
    except KeyboardInterrupt:
        pass
    finally:
        app.stop()
        logger.info("Validation Complete.")
