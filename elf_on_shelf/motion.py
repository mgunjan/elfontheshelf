import time
import random
import threading
import numpy as np

class RobotController:
    def __init__(self, reachy):
        self.reachy = reachy
        self.is_frozen = False
        self._stop_event = threading.Event()

    def set_compliant(self, compliant=False):
        """Set compliance for head and antennas."""
        for motor in self.reachy.head.motors:
            motor.compliant = compliant
        # Check if antennas exist (some models might not have them mapped same way)
        if hasattr(self.reachy, 'antenna'):
             for motor in self.reachy.antenna.motors:
                motor.compliant = compliant

    def freeze(self):
        """Immediately stop movement and hold position."""
        if self.is_frozen:
            return
        self.is_frozen = True
        # To freeze, we ensure motors are stiff (not compliant) and stop sending new targets.
        # Assuming Reachy maintains position when target is not updated if stiff.
        # We can also read current position and set it as target to be sure.
        for motor in self.reachy.head.motors:
            motor.target_position = motor.present_position
        
    def unfreeze(self):
        """Resume ability to move."""
        self.is_frozen = False

    def look_at(self, x, y, z, duration=1.0):
        if self.is_frozen: return
        self.reachy.head.look_at(x, y, z, duration=duration)

    def scan_idle(self):
        """Perform a random small movement to look alive."""
        if self.is_frozen: return
        
        # Random gentle head movements
        x = random.uniform(0.3, 0.5)
        y = random.uniform(-0.3, 0.3)
        z = random.uniform(-0.2, 0.2)
        
        try:
            self.reachy.head.look_at(x=x, y=y, z=z, duration=1.5)
            self.wiggle_antennas()
        except Exception:
            pass # Ignore kinematics errors

    def wiggle_antennas(self):
        if self.is_frozen: return
        # Simple wiggle
        if hasattr(self.reachy, 'antenna'):
            # Placeholder for antenna control
            pass

    def perform_scan_animation(self):
        """Animation for Naughty/Nice scanning."""
        if self.is_frozen: return # Though this might be overridden by caller
        
        # Tilt head up and down
        for _ in range(3):
            self.reachy.head.l_antenna.goal_position = 45
            self.reachy.head.r_antenna.goal_position = -45
            time.sleep(0.3)
            self.reachy.head.l_antenna.goal_position = -10
            self.reachy.head.r_antenna.goal_position = 10
            time.sleep(0.3)

    def express_joy(self):
        """Happy animation."""
        # Nodding
        self.reachy.head.look_at(0.5, 0, 0, duration=0.5)
        time.sleep(0.5)
        self.reachy.head.look_at(0.5, 0, -0.2, duration=0.3)
        time.sleep(0.3)
        self.reachy.head.look_at(0.5, 0, 0, duration=0.3)

    def express_sadness(self):
        """Sad animation."""
        # Look down and shake head slightly
        self.reachy.head.look_at(0.4, 0, -0.4, duration=1.0)
        time.sleep(1.0)
        # Shake
        current_pos = self.reachy.head.neck_yaw.present_position
        self.reachy.head.neck_yaw.target_position = current_pos + 10
        time.sleep(0.5)
        self.reachy.head.neck_yaw.target_position = current_pos - 10
        time.sleep(0.5)
        self.reachy.head.neck_yaw.target_position = current_pos
