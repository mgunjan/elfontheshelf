import time
import threading
import sys
import os

try:
    from reachy_sdk import ReachySDK
except ImportError:
    ReachySDK = None

# Try to import ReachyMiniApp, mock if missing
try:
    from reachy_mini.app import ReachyMiniApp
except ImportError:
    class ReachyMiniApp:
        def __init__(self, app_path=None):
            self.app_path = app_path
            self.reachy = None
        def is_running(self):
            return True

from .vision import VisionSystem
from .audio import AudioSystem
from .motion import RobotController
from .behaviors.sentry import SentryMode
from .behaviors.scanner import NaughtyNiceScanner

class MockMotor:
    def __init__(self):
        self.compliant = False
        self.present_position = 0.0
        self.target_position = 0.0

class MockReachy:
    def __init__(self):
        print("[Mock] Initialized Mock Reachy")
        self.head = self._SubPart()
        self.antenna = self._SubPart()
        
    class _SubPart:
        def __init__(self):
            self.motors = [MockMotor() for _ in range(3)]
            self.l_antenna = MockMotor()
            self.r_antenna = MockMotor()
            self.neck_yaw = MockMotor()
        def look_at(self, x, y, z, duration):
            print(f"[Mock] Looking at {x}, {y}, {z}")

class ElfApp(ReachyMiniApp):
    def __init__(self, reachy_sdk=None, host='localhost'):
        super().__init__()
        self.reachy = reachy_sdk
        self._local_sdk = False
        
        # If no SDK provided (running standalone), try to connect
        if self.reachy is None:
            if ReachySDK:
                try:
                    self.reachy = ReachySDK(host=host)
                    self._local_sdk = True
                except Exception:
                    pass
            
            if self.reachy is None:
                print("Using Mock Reachy Backend")
                self.reachy = MockReachy()

        self.vision = VisionSystem()
        self.audio = AudioSystem()
        self.motion = RobotController(self.reachy)
        
        self.sentry = SentryMode(self.motion, self.vision)
        self.scanner = NaughtyNiceScanner(self.motion, self.audio)
        
        self.running = False
        self._main_thread = None

    def run(self):
        print("Starting Elf on the Shelf App...")
        self.vision.start()
        self.audio.start()
        self.running = True
        
        # The Reachy app runner might expect run() to block or validly return boolean
        # We will loop here.
        try:
            while self.is_running() and self.running:
                # Priority: Scanner > Sentry
                if self.scanner.check_trigger():
                    self.scanner.run_sequence()
                    self.sentry.last_saw_face_time = 0 
                else:
                    self.sentry.update()
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            self.stop()
        
        return True

    def stop(self):
        self.running = False
        self.vision.stop()
        self.audio.stop()
        print("App stopped.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost", help="Reachy IP address or hostname")
    args = parser.parse_args()

    app = ElfApp(host=args.host)
    app.run()
