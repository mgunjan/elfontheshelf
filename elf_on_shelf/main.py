"""Elf on the Shelf - Magic Elf Mode for Reachy Mini."""

import time
import random
import threading
from typing import Optional

from reachy_mini import ReachyMini, ReachyMiniApp

from .vision import VisionSystem
from .audio_generator import sound_player
from .motion import RobotController


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
        
        # Initialize subsystems
        print("\n[Init] Initializing subsystems...")
        
        # Enable motors
        try:
            print("[Init] Enabling motors...")
            reachy_mini.enable_motors()
            time.sleep(0.5)
        except Exception as e:
            print(f"[Init] Warning - motor enable: {e}")
        
        # Initialize media (audio/camera)
        try:
            print("[Init] Starting media pipeline...")
            reachy_mini.media.start_recording()
            time.sleep(0.5)
            reachy_mini.media.start_playing()
            time.sleep(1.0)  # Give media time to fully initialize
            print("[Init] ✅ Media pipeline ready")
        except Exception as e:
            print(f"[Init] ⚠️  Media initialization warning: {e}")
        
        # Set up vision system
        vision = VisionSystem(reachy_mini=reachy_mini)
        vision.start()
        print("[Init] ✅ Vision system started")
        
        # Set up audio
        sound_player.set_reachy(reachy_mini)
        print("[Init] ✅ Audio system ready")
        
        # Set up motion controller
        controller = RobotController(reachy_mini)
        print("[Init] ✅ Motion controller ready")
        
        # State tracking
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
        
        # Main behavior loop
        try:
            while not stop_event.is_set():
                current_time = time.time()
                face_detected = vision.is_face_present()
                
                # Detect state transitions
                if face_detected and not was_face_detected:
                    # FACE JUST APPEARED - SURPRISE!
                    print("\n👀 FACE DETECTED! Freezing with surprise...")
                    controller.express_surprise()
                    sound_player.play_surprise()
                    was_face_detected = True
                    
                elif face_detected and was_face_detected:
                    # FACE STILL PRESENT - STAY FROZEN
                    controller.freeze()
                    
                elif not face_detected and was_face_detected:
                    # FACE DISAPPEARED - RESUME BEING ALIVE
                    print("\n😊 Face gone! Resuming alive mode...")
                    controller.unfreeze()
                    was_face_detected = False
                    # Reset timers
                    last_movement_time = current_time
                    next_movement_delay = random.uniform(3.0, 6.0)
                    last_jingle_time = current_time
                    next_jingle_delay = random.uniform(10.0, 15.0)
                    
                else:
                    # NO FACE - ACT ALIVE
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
                
                # Check for stop event frequently
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n[Shutdown] Keyboard interrupt received")
        except Exception as e:
            print(f"\n\n[Error] Unexpected error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup
            print("\n[Shutdown] Cleaning up...")
            
            try:
                vision.stop()
                print("[Shutdown] ✅ Vision system stopped")
            except Exception as e:
                print(f"[Shutdown] Vision stop error: {e}")
            
            try:
                controller.unfreeze()
                print("[Shutdown] ✅ Robot unfrozen")
            except Exception as e:
                print(f"[Shutdown] Unfreeze error: {e}")
            
            try:
                reachy_mini.disable_motors()
                print("[Shutdown] ✅ Motors disabled")
            except Exception as e:
                print(f"[Shutdown] Motor disable error: {e}")
            
            print("\n" + "=" * 60)
            print("🎄 Elf on the Shelf - Goodbye! 🎄")
            print("=" * 60)

