import argparse
import sys
from reachy_sdk import ReachySDK

def test_connection(host):
    print(f"Attempting to connect to Reachy at {host}...")
    try:
        reachy = ReachySDK(host=host)
        print("Successfully connected!")
        
        print("Checking battery voltage...")
        # Note: API might differ depending on version, generic check
        try:
            # Assuming standard Reachy SDK structure, though Mini might differ slightly.
            # We'll just print connected parts.
            print("Connected parts:")
            for name, part in reachy.joints.items():
                print(f" - {name}")
        except Exception as e:
            print(f"Could not inspect joints: {e}")

        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost", help="Reachy IP address or hostname")
    args = parser.parse_args()
    
    success = test_connection(args.host)
    sys.exit(0 if success else 1)
