import argparse
import sys
import time
try:
    from reachy_mini import ReachyMini
except ImportError:
    print("Error: reachy-mini SDK not found. Install it first.")
    sys.exit(1)

def test_connection(host):
    print(f"Attempting to connect to Reachy Mini (Mock Host param: {host})...")
    
    # ReachyMini SDK uses Zenoh discovery. "host" param mainly toggles localhost vs network.
    is_localhost = "localhost" in host or "127.0.0.1" in host
    
    try:
        print(f"Initializing ReachyMini(localhost_only={is_localhost})...")
        print("Waiting for Zenoh discovery (this may take a few seconds)...")
        
        reachy = ReachyMini(robot_name='reachy_mini', localhost_only=is_localhost)
        
        print("✅ Successfully connected via Zenoh!")
        
        # Simple movement check
        print("Running simple movement check...")
        current_pos = reachy.get_current_head_pose()
        print(f"Current Head Pose: {current_pos[0][3]:.2f}, {current_pos[1][3]:.2f}, {current_pos[2][3]:.2f}")
        
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Tip: Ensure your computer is on the same Wi-Fi as 'reachy-mini'.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost", help="Reachy IP/Hostname (Used to toggle local/remote mode)")
    args = parser.parse_args()
    
    success = test_connection(args.host)
    sys.exit(0 if success else 1)
