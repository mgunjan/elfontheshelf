
import time
import argparse
from reachy_mini import ReachyMini

def main():
    parser = argparse.ArgumentParser(description="Validate Reachy Mini audio connectivity.")
    parser.add_argument("--host", default="reachy-mini.local", help="Robot hostname or IP")
    args = parser.parse_args()

    print(f"Connecting to robot at {args.host}...")
    try:
        # Connect to remote robot
        reachy = ReachyMini(localhost_only=False, timeout=10.0)
        print("Connected!")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    print("Checking audio status...")
    if reachy.media.audio is None:
        print("Audio system is NOT initialized in SDK.")
        return

    print("Attempting to play built-in 'wake_up.wav' on robot...")
    try:
        reachy.media.play_sound("wake_up.wav")
        print("Sound command sent. Listen to the robot!")
    except Exception as e:
        print(f"Error playing sound: {e}")

    print("\nWaiting 5 seconds for sound to finish...")
    time.sleep(5)

    reachy.media.close()

if __name__ == "__main__":
    main()
