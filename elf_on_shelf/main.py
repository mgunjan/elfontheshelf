"""Elf on the Shelf - Magic Elf Mode for Reachy Mini."""

import sys
import time
import random
import threading
import traceback
from typing import Optional

# Ensure standard output is flushed immediately for logs
sys.stdout.reconfigure(line_buffering=True)

try:
    from reachy_mini import ReachyMini, ReachyMiniApp
except ImportError:
    print("CRITICAL: Could not import reachy_mini module!")
    sys.exit(1)

# Import other modules - allow failure for debugging
try:
    from .vision import VisionSystem
    from .audio_generator import sound_player
    from .motion import RobotController
except ImportError as e:
    print(f"CRITICAL: Failed to import local modules: {e}")
    # Define dummy classes to prevent ImportErrors from stopping the app manager immediately
    VisionSystem = None
    sound_player = None
    RobotController = None


class ElfOnShelf(ReachyMiniApp):
    """
    Magic Elf Mode: Reachy acts alive when no one is watching,
    but freezes with surprise when a face is detected.
    """
    
    custom_app_url: Optional[str] = None
    request_media_backend: Optional[str] = None  # Let SDK auto-detect

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event) -> None:
        """Main application loop implementing Magic Elf Mode."""
        print("=" * 60)
        print("🎄 ELF ON THE SHELF - MAGIC ELF MODE 🎄")
        print("=" * 60)
        
        # Check for imports
        if VisionSystem is None or sound_player is None or RobotController is None:
            print("❌ Start aborted: Local modules failed to import.")
            return

        # Initialize subsystems
        print("\n[Init] Initializing subsystems...")
        
        # 1. Enable motors
        try:
            print("[Init] Enabling motors...")
            reachy_mini.enable_motors()
            time.sleep(0.5)
        except Exception as e:
            print(f"[Init] Warning - motor enable: {e}")
        
        # 2. Initialize media (audio/camera)
        try:
            print("[Init] Starting media pipeline...")
            if reachy_mini.media:
                reachy_mini.media.start_recording()
                time.sleep(0.5)
                reachy_mini.media.start_playing()
                time.sleep(1.0)
                print("[Init] ✅ Media pipeline ready")
            else:
                print("[Init] ⚠️  Media manager is None!")
        except Exception as e:
            print(f"[Init] ⚠️  Media initialization warning: {e}")
        
        # 3. Set up subsystems
        try:
            vision = VisionSystem(reachy_mini=reachy_mini)
            vision.start()
            print("[Init] ✅ Vision system started")
            
            sound_player.set_reachy(reachy_mini)
            print("[Init] ✅ Audio system ready")
            
            controller = RobotController(reachy_mini)
            print("[Init] ✅ Motion controller ready")
        except Exception as e:
            print(f"[Init] ❌ Subsystem initialization failed: {e}")
            return
        
        # State variables
        was_face_detected = False
        last_jingle_time = time.time()
        next_jingle_delay = random.uniform(10.0, 15.0)
        last_movement_time = time.time()
        next_movement_delay = random.uniform(3.0, 6.0)
        
        print("\n" + "=" * 60)
        print("🎅 MAGIC ELF MODE ACTIVE!")
        print("   - No face: Robot acts alive (moves, plays jingles)")
        print("   - Face detected: FREEZE with surprise!")
        print("=" * 60 + "\n")
        
        try:
            while not stop_event.is_set():
                current_time = time.time()
                
                # Check for face (safely)
                face_detected = vision.is_face_present()
                
                # State Logic
                if face_detected and not was_face_detected:
                    # Case 1: Just caught!
                    print("\n👀 FACE DETECTED! Freezing with surprise...")
                    controller.express_surprise()
                    sound_player.play_surprise()
                    was_face_detected = True
                    
                elif face_detected and was_face_detected:
                    # Case 2: Still being watched
                    controller.freeze()
                    
                elif not face_detected and was_face_detected:
                    # Case 3: Coast is clear
                    print("\n😊 Face gone! Resuming alive mode...")
                    controller.unfreeze()
                    was_face_detected = False
                    # Reset timers to avoid instant action
                    last_movement_time = current_time
                    next_movement_delay = random.uniform(3.0, 6.0)
                    last_jingle_time = current_time
                    next_jingle_delay = random.uniform(10.0, 15.0)
                    
                else:
                    # Case 4: Idling (Alive mode)
                    # Periodic movements
                    if current_time - last_movement_time > next_movement_delay:
                        print("🤖 Acting alive (looking around)...")
                        controller.act_alive()
                        last_movement_time = current_time
                        next_movement_delay = random.uniform(3.0, 6.0)
                    
                    # Periodic jingles
                    if current_time - last_jingle_time > next_jingle_delay:
                        print("🎵 Humming jingle bells...")
                        sound_player.play_jingle_bells()
                        last_jingle_time = current_time
                        next_jingle_delay = random.uniform(10.0, 15.0)
                
                # Small sleep to prevent CPU hogging
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n[Shutdown] Keyboard interrupt")
        except Exception as e:
            print(f"\n[Error] Main loop error: {e}")
            traceback.print_exc()
        finally:
            print("\n[Shutdown] Cleaning up...")
            try:
                vision.stop()
                controller.unfreeze()
                reachy_mini.disable_motors()
            except Exception:
                pass
            print("🎄 Elf on the Shelf - Goodbye! 🎄")


if __name__ == "__main__":
    app = ElfOnShelf()
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()



