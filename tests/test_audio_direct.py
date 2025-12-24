#!/usr/bin/env python3
"""Minimal audio test - runs on the robot directly."""

import time
from reachy_mini import ReachyMini

def main():
    print("=" * 50)
    print("DIRECT AUDIO TEST")
    print("=" * 50)
    
    print("Connecting to robot...")
    reachy = ReachyMini(media_backend="gstreamer")
    print(f"Connected! Media backend: {reachy.media_manager.backend}")
    
    print(f"Audio initialized: {reachy.media.audio is not None}")
    print(f"Camera initialized: {reachy.media.camera is not None}")
    
    if reachy.media.audio is None:
        print("ERROR: Audio is None!")
        return
    
    print("\nStarting media pipelines...")
    try:
        reachy.media.start_recording()
        print("✅ start_recording() OK")
    except Exception as e:
        print(f"❌ start_recording() failed: {e}")
    
    try:
        reachy.media.start_playing()
        print("✅ start_playing() OK")
    except Exception as e:
        print(f"❌ start_playing() failed: {e}")
    
    time.sleep(1)
    
    print("\nPlaying wake_up.wav...")
    try:
        reachy.media.play_sound("wake_up.wav")
        print("✅ play_sound() called")
    except Exception as e:
        print(f"❌ play_sound() failed: {e}")
    
    print("\nWaiting 3 seconds for sound to play...")
    time.sleep(3)
    
    print("\nDone!")
    reachy.media.close()

if __name__ == "__main__":
    main()
