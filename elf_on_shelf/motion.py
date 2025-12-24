import time
import random
import threading

class RobotController:
    def __init__(self, reachy):
        self.reachy = reachy
        self.is_frozen = False
        self._stop_event = threading.Event()

    def set_compliant(self, compliant=False):
        """Set compliance for head and antennas."""
        if compliant:
            self.reachy.disable_motors()
        else:
            self.reachy.enable_motors()

    def freeze(self):
        """Immediately stop movement and hold position."""
        if self.is_frozen:
            return
        self.is_frozen = True
        # Read current head pose and set it as target to hold it
        try:
            current_head = self.reachy.get_current_head_pose()
            current_antennas = self.reachy.get_present_antenna_joint_positions()
            self.reachy.set_target(head=current_head, antennas=current_antennas)
        except Exception as e:
            print(f"[Motion] Freeze error: {e}")
        
    def express_surprise(self):
        """Show a 'Guilty/Shocked' expression before freezing."""
        if self.is_frozen: return
        
        # 1. Pop antennas out (Shock!)
        try:
            # Wide antennas = Shock
            self.reachy.set_target(antennas=[0.6, -0.6]) # Instant move
            # Small delay to let user see the shock
            time.sleep(0.2)
        except Exception as e:
            print(f"[Motion] Express surprise error: {e}")
        
        # 2. Then Freeze
        self.freeze()
        
    def unfreeze(self):
        """Resume ability to move."""
        self.is_frozen = False

    def look_at(self, x, y, z, duration=1.0):
        if self.is_frozen: return
        self.reachy.look_at_world(x, y, z, duration=duration)

    def act_alive(self):
        """Perform random, jolly movements to simulate being alive."""
        if self.is_frozen: return
        
        # Random gentle head movements with a "jolly" cadence
        x = random.uniform(0.3, 0.5)
        y = random.uniform(-0.4, 0.4)
        z = random.uniform(-0.1, 0.3)
        duration = random.uniform(1.0, 2.5)

        try:
            self.reachy.look_at_world(x=x, y=y, z=z, duration=duration)
            
            # Occasionally wiggle antennas happily
            if random.random() > 0.6:
                self.wiggle_antennas()
        except Exception as e:
            print(f"[Motion] Act alive error: {e}")

    def wiggle_antennas(self):
        if self.is_frozen: return
        # Jolly wiggle
        try:
            current = self.reachy.get_present_antenna_joint_positions()
            # Wiggle around current frame or neutral
            self.reachy.goto_target(antennas=[0.5, -0.5], duration=0.2)
            time.sleep(0.2)
            self.reachy.goto_target(antennas=[-0.5, 0.5], duration=0.2)
            time.sleep(0.2)
            self.reachy.goto_target(antennas=[0.0, 0.0], duration=0.2) # Return to neutral
        except Exception as e:
            print(f"[Motion] Wiggle antennas error: {e}")

    def perform_scan_animation(self):
        """Animation for Naughty/Nice scanning."""
        if self.is_frozen: return
        
        # Tilt antennas
        for _ in range(3):
            self.reachy.goto_target(antennas=[0.8, -0.8], duration=0.3)
            time.sleep(0.3)
            self.reachy.goto_target(antennas=[-0.2, 0.2], duration=0.3)
            time.sleep(0.3)

    def express_joy(self):
        """Happy animation."""
        # Nodding
        self.reachy.look_at_world(0.5, 0, 0, duration=0.5)
        time.sleep(0.5)
        self.reachy.look_at_world(0.5, 0, -0.2, duration=0.3)
        time.sleep(0.3)
        self.reachy.look_at_world(0.5, 0, 0, duration=0.3)

    def express_sadness(self):
        """Sad animation."""
        # Look down and shake head
        self.reachy.look_at_world(0.4, 0, -0.4, duration=1.0)
        time.sleep(1.0)
        
        # Shake implementation via look_at (approximate)
        # Ideally would use joint control but look_at is safer
        self.reachy.look_at_world(0.4, 0.1, -0.4, duration=0.3)
        time.sleep(0.3)
        self.reachy.look_at_world(0.4, -0.1, -0.4, duration=0.3)
        time.sleep(0.3)
        self.reachy.look_at_world(0.4, 0, -0.4, duration=0.3)
