import time
import random
import threading

class NaughtyNiceScanner:
    def __init__(self, controller, audio):
        self.controller = controller
        self.audio = audio
        self.is_active = False

    def check_trigger(self):
        """Check if triggered. If so, return True and set internal active state."""
        if self.audio.is_triggered():
            self.is_active = True
            return True
        return False

    def run_sequence(self):
        """Blocking sequence for the scanner game."""
        if not self.is_active:
            return

        print("Scanner triggered!")
        # 1. Scanning Phase
        # self.controller.unfreeze() # Ensure we can move
        self.controller.perform_scan_animation()
        
        # 2. Decision Phase
        result = random.choice(["nice", "naughty"])
        print(f"Verdict: {result.upper()}")
        
        # 3. Response Phase (Animation + Sound placeholder)
        if result == "nice":
            self.controller.express_joy()
            # TODO: Play nice sound
        else:
            self.controller.express_sadness()
            # TODO: Play naughty sound
            
        time.sleep(1.0) # Pause for effect
        self.is_active = False
        print("Scanner finished.")
