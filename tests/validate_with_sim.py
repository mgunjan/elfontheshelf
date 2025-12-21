import time
import subprocess
import sys
import logging
import threading
from reachy_mini import ReachyMini

# Configuration
DAEMON_PORT = 8000  # API Port
ZENOH_PORT = 7447
HEADLESS = True
TIMEOUT = 30 # Seconds to wait for simulator to start

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("validator")

def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_simulator():
    """Starts the Reachy Mini simulator in a subprocess."""
    cmd = [
        "uv", "run", "mjpython", "-m", "reachy_mini.daemon.app.main",
        "--sim",
        "--scene", "empty",  # Use empty scene for speed
    ]
    
    if HEADLESS:
        cmd.append("--headless")
        
    logger.info(f"Starting simulator: {' '.join(cmd)}")
    
    # Start process
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return process

def wait_for_simulator(timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        if is_port_in_use(DAEMON_PORT):
            logger.info("Simulator daemon detected on port 8000.")
            return True
        time.sleep(1)
    return False

def run_validation():
    logger.info("Connecting to Reachy Mini (no media)...")
    try:
        robot = ReachyMini(robot_name="reachy_mini", localhost_only=True, media_backend="no_media")
        
        logger.info("Checking initial head pose...")
        initial_pose = robot.get_current_head_pose()
        logger.info(f"Initial Pose: {initial_pose}")
        
        logger.info("Moving head...")
        # Move head slightly
        robot.look_at_world(x=0.5, y=0.0, z=0.0, duration=1.0)
        time.sleep(1.5) # Wait for move
        
        new_pose = robot.get_current_head_pose()
        logger.info(f"New Pose: {new_pose}")
        
        # Simple check: verify it's not identical to initial (it moved)
        if (initial_pose == new_pose).all():
             logger.error("Robot head did not move!")
             return False
             
        logger.info("Validation Successful! Robot moved.")
        return True
        
    except Exception as e:
        logger.error(f"Validation failed with error: {e}")
        return False
    finally:
         # Cleanup if needed
         pass

def main():
    sim_process = None
    started_sim = False
    
    try:
        # 1. Check if simulator is running
        if not is_port_in_use(DAEMON_PORT):
            logger.info("Simulator not running. Starting headless...")
            sim_process = start_simulator()
            started_sim = True
            
            if not wait_for_simulator(TIMEOUT):
                logger.error("Timed out waiting for simulator to start.")
                sys.exit(1)
            
            # Give it a few more seconds to fully initialize Zenoh
            time.sleep(5) 
        else:
            logger.info("Simulator already running. Using existing instance.")

        # 2. Run Validation
        success = run_validation()
        
        if success:
            logger.info("✅ VALIDATION PASSED")
            sys.exit(0)
        else:
            logger.error("❌ VALIDATION FAILED")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Interrupted.")
    finally:
        # 3. Cleanup
        if started_sim and sim_process:
            logger.info("Stopping simulator process...")
            sim_process.terminate()
            sim_process.wait()

if __name__ == "__main__":
    main()
