import time
import random

class SentryMode:
    def __init__(self, controller, vision):
        self.controller = controller
        self.vision = vision
        self.last_saw_face_time = 0
        self.freeze_buffer_duration = 2.0  # Seconds to remain frozen after face triggers
        self.next_idle_move_time = 0

    def update(self):
        """
        Called periodically (e.g. 10Hz).
        Returns True if the Sentry logic is 'active' (controlling the robot), 
        False if it yields control (not strictly used here but good for composition).
        """
        if self.vision.is_face_present():
            self.last_saw_face_time = time.time()
            self.controller.freeze()
            # print("Face seen! Freezing.")
            return

        # If we saw a face recently, stay frozen
        if time.time() - self.last_saw_face_time < self.freeze_buffer_duration:
            self.controller.freeze()
            return

        # Otherwise, we are free to move.
        # Ensure we are unfrozen
        self.controller.unfreeze()
        
        # Periodic idle movements
        if time.time() > self.next_idle_move_time:
            self.controller.act_alive()
            # Schedule next move in 3-8 seconds
            self.next_idle_move_time = time.time() + random.uniform(3.0, 8.0)
