"""Minimal audio test app - just plays sound on startup."""

import time
import threading
from typing import Optional

from reachy_mini import ReachyMini, ReachyMiniApp


class ElfOnShelf(ReachyMiniApp):
    """Minimal app to test audio."""
    
    custom_app_url: Optional[str] = None
    request_media_backend: Optional[str] = None  # Let SDK auto-detect

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event) -> None:
        """Just play sound and wiggle antennas."""
        print("=" * 50)
        print("MINIMAL AUDIO TEST START")
        print("=" * 50)
        
        # Log everything about media
        print(f"Media manager: {reachy_mini.media}")
        print(f"Media backend: {reachy_mini.media_manager.backend if hasattr(reachy_mini, 'media_manager') else 'unknown'}")
        print(f"Audio object: {reachy_mini.media.audio}")
        print(f"Camera object: {reachy_mini.media.camera}")
        
        # Try to play sound immediately
        print("\n[TEST] Attempting play_sound('wake_up.wav')...")
        try:
            reachy_mini.media.play_sound("wake_up.wav")
            print("[TEST] ✅ play_sound() completed without exception")
        except Exception as e:
            print(f"[TEST] ❌ play_sound() FAILED: {type(e).__name__}: {e}")
        
        # Wait for sound
        time.sleep(2)
        
        # Try after calling start_playing
        print("\n[TEST] Calling start_recording() + start_playing()...")
        try:
            reachy_mini.media.start_recording()
            print("[TEST] ✅ start_recording() OK")
        except Exception as e:
            print(f"[TEST] ❌ start_recording() FAILED: {e}")
            
        try:
            reachy_mini.media.start_playing()
            print("[TEST] ✅ start_playing() OK")
        except Exception as e:
            print(f"[TEST] ❌ start_playing() FAILED: {e}")
        
        time.sleep(1)
        
        print("\n[TEST] Attempting play_sound('go_sleep.wav') AFTER pipeline init...")
        try:
            reachy_mini.media.play_sound("go_sleep.wav")
            print("[TEST] ✅ play_sound() completed without exception")
        except Exception as e:
            print(f"[TEST] ❌ play_sound() FAILED: {type(e).__name__}: {e}")
        
        time.sleep(2)
        
        # Wiggle antennas to show we're done
        print("\n[TEST] Wiggling antennas to signal end...")
        try:
            reachy_mini.goto_target(antennas=[1.0, 1.0], duration=0.5)
            time.sleep(1)
            reachy_mini.goto_target(antennas=[0.0, 0.0], duration=0.5)
        except:
            pass
        
        print("\n" + "=" * 50)
        print("MINIMAL AUDIO TEST COMPLETE")
        print("=" * 50)
        
        # Keep running briefly
        time.sleep(3)
