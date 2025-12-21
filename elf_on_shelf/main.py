"""Elf on the Shelf App for Reachy Mini.

Magic Elf Mode: The robot acts "alive" when no one is watching,
but freezes instantly when a face is detected with a surprise expression.
"""

import time
import threading
import random

from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.utils import create_head_pose

from .vision import VisionSystem
from .motion import RobotController
from .audio_generator import sound_player


class MagicMode:
    """
    Magic Elf Mode:
    - If Face Detected: FREEZE immediately with surprise expression
    - If No Face: Act alive (random movements, occasional jingle bells)
    """
    def __init__(self, motion_ctrl, vision_sys):
        self.motion = motion_ctrl
        self.vision = vision_sys
        self.is_frozen = False

    def update(self):
        faces = self.vision.get_faces()
        
        if faces:
            # Face detected! Freeze!
            if not self.is_frozen:
                print("[MagicMode] Face detected! FREEZE!")
                sound_player.play_surprise()
                self.motion.express_surprise()
                self.is_frozen = True
        else:
            # No face detected. Come alive.
            if self.is_frozen:
                print("[MagicMode] Coast clear. Unfreezing...")
                self.motion.unfreeze()
                self.is_frozen = False
            
            # Perform alive behaviors if not frozen
            self.motion.act_alive()
            # Chance to play jingle bells (~5% per loop)
            if random.random() > 0.95:
                threading.Thread(target=sound_player.play_jingle_bells, daemon=True).start()


class ElfOnShelf(ReachyMiniApp):
    """Elf on the Shelf App - Magic Elf Mode.
    
    When run from the Reachy Mini dashboard, the robot will:
    - Look around randomly and wiggle antennas when no one is watching
    - Play "Jingle Bells" occasionally
    - Freeze instantly with a "Surprise!" expression when a face is detected
    """
    
    # Optional: URL to a custom configuration page for the app
    custom_app_url: str | None = None

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event):
        """Main app loop - called by the dashboard.
        
        Args:
            reachy_mini: Already connected ReachyMini instance
            stop_event: Event to signal app shutdown
        """
        print("🎄 Starting Elf on the Shelf App (Magic Mode)... 🎄")
        
        # Initialize subsystems
        vision = VisionSystem(reachy_mini=reachy_mini)
        motion = RobotController(reachy_mini)
        sound_player.set_reachy(reachy_mini)
        
        magic_mode = MagicMode(motion, vision)
        
        # Start vision processing
        vision.start()
        
        try:
            while not stop_event.is_set():
                magic_mode.update()
                time.sleep(0.1)
        except Exception as e:
            print(f"[ElfApp] Error: {e}")
        finally:
            vision.stop()
            print("🎄 Elf on the Shelf App stopped. 🎄")


# For standalone testing (python -m elf_on_shelf.main)
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Elf on the Shelf for Reachy Mini")
    parser.add_argument("--host", default="localhost", help="Reachy hostname (localhost or reachy-mini.local)")
    args = parser.parse_args()
    
    print("Running in standalone mode...")
    print("For proper deployment, use: reachy-mini-app-assistant publish")
    
    # Connect manually for standalone testing
    is_local = (args.host == 'localhost' or args.host == '127.0.0.1')
    print(f"Connecting to Reachy Mini (localhost_only={is_local})...")
    
    try:
        reachy = ReachyMini(robot_name='reachy_mini', localhost_only=is_local)
        print("✅ Connected!")
        
        stop_event = threading.Event()
        app = ElfOnShelf()
        
        try:
            app.run(reachy, stop_event)
        except KeyboardInterrupt:
            print("\nStopping...")
            stop_event.set()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Make sure the Reachy Mini daemon is running.")
