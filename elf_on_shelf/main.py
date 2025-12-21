import time
import threading
import random
import sys
import os

try:
    from reachy_mini import ReachyMini
except ImportError:
    ReachyMini = None

# Try to import ReachyMiniApp, mock if missing
try:
    from reachy_mini.apps.app import ReachyMiniApp
except ImportError:
    class ReachyMiniApp:
        def __init__(self, app_path=None):
            self.app_path = app_path
            self.reachy = None
        def is_running(self):
            return True

from .vision import VisionSystem
from .vision import VisionSystem
# from .audio import AudioSystem # Removed as per user request
from .motion import RobotController
from .behaviors.sentry import SentryMode
# from .behaviors.scanner import NaughtyNiceScanner # Removed
from .audio_generator import sound_player

class MockReachy:
    def __init__(self):
        print("[Mock] Initialized Mock Reachy")
    
    def look_at_world(self, x, y, z, duration=1.0):
        print(f"[Mock] Looking at {x}, {y}, {z}")

    def goto_target(self, head=None, antennas=None, duration=1.0):
        if antennas:
            print(f"[Mock] Moving antennas to {antennas}")

    def get_current_head_pose(self):
        return [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    
    def get_present_antenna_joint_positions(self):
        return [0.0, 0.0]
    
    def enable_motors(self):
        print("[Mock] Motors Enabled")

    def disable_motors(self):
        print("[Mock] Motors Disabled")
    
    def set_target(self, head=None, antennas=None):
        pass

class MagicMode:
    """
    Magic Elf Mode:
    - If Face Detected: FREEZE immediately.
    - If No Face: Act alive (random movements).
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
            # Chance to hum jingle bells
            if random.random() > 0.95:
                threading.Thread(target=sound_player.play_jingle_bells).start()

class ElfApp(ReachyMiniApp):
    def __init__(self, reachy_mini=None, host='localhost'):
        super().__init__()
        self.reachy = reachy_mini
        self._local_sdk = False
        
        # If no SDK provided (running standalone), try to connect
        if self.reachy is None:
            if ReachyMini:
                try:
                    # spawn_daemon=False assuming it's running externally (sim or real)
                    self.reachy = ReachyMini(robot_name='reachy_mini', localhost_only=(host=='localhost'))
                    self._local_sdk = True
                except Exception as e:
                    print(f"Connection failed: {e}")
            
            if self.reachy is None:
                print("Using Mock Reachy Backend")
                self.reachy = MockReachy()

        self.vision = VisionSystem()
        # self.audio = AudioSystem() # Input disabled
        self.motion = RobotController(self.reachy)
        
        # Determine mode logic. Defaulting to MagicMode as per user request.
        # We can keep SentryMode/Scanner as alternatives or sub-features.
        # For this request, MagicMode is the primary "Elf" behavior.
        self.magic_mode = MagicMode(self.motion, self.vision)
        # self.scanner = NaughtyNiceScanner(self.motion, self.audio) # Removed
        
        self.running = False
        self._main_thread = None

    def run(self):
        print("Starting Elf on the Shelf App (Magic Mode)...")
        self.vision.start()
        # self.audio.start()
        self.running = True
        
        # The Reachy app runner might expect run() to block or validly return boolean
        # We will loop here.
        try:
            while not self.stop_event.is_set() and self.running:
                self.magic_mode.update()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            self.stop()
        
        return True

    def stop(self):
        self.running = False
        self.vision.stop()
        # self.audio.stop()
        print("App stopped.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost", help="Reachy IP address or hostname")
    args = parser.parse_args()

    app = ElfApp(host=args.host)
    app.run()
