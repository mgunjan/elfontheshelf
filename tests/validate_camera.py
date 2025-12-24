
import cv2
import time
import argparse
from reachy_mini import ReachyMini

def main():
    parser = argparse.ArgumentParser(description="Validate Reachy Mini camera connectivity.")
    parser.add_argument("--host", default="reachy-mini.local", help="Robot hostname or IP")
    args = parser.parse_args()

    print(f"Connecting to robot at {args.host}...")
    try:
        # We use a 10s timeout for connection
        # and we explicitly request the WebRTC backend for remote connection
        reachy = ReachyMini(localhost_only=False, timeout=10.0)
        print("Connected!")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    print("Checking camera status...")
    if reachy.media.camera is None:
        print("Camera is NOT initialized in SDK.")
        return

    print("Attempting to grab 5 frames...")
    frames_grabbed = 0
    for i in range(5):
        frame = reachy.media.get_frame()
        if frame is not None:
            print(f"Frame {i+1} received! Shape: {frame.shape}")
            frames_grabbed += 1
            # Save the first frame to a file if possible
            if frames_grabbed == 1:
                cv2.imwrite("camera_test.jpg", frame)
                print("First frame saved as 'camera_test.jpg'")
        else:
            print(f"Frame {i+1} is None.")
        time.sleep(0.5)

    if frames_grabbed > 0:
        print(f"SUCCESS: Grabbed {frames_grabbed}/5 frames.")
    else:
        print("FAILURE: No frames received.")

    reachy.media.close()

if __name__ == "__main__":
    main()
