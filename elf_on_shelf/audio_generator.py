"""Audio generator that plays sounds on Reachy Mini robot only."""

import time
import threading


class SoundGenerator:
    """Sound generator that plays audio on the robot."""
    
    def __init__(self, reachy_mini=None):
        """Initialize sound generator.
        
        Args:
            reachy_mini: ReachyMini instance for robot audio.
        """
        self.reachy_mini = reachy_mini
        self._lock = threading.Lock()

    def set_reachy(self, reachy_mini):
        """Set the ReachyMini instance for robot audio."""
        self.reachy_mini = reachy_mini

    def _can_use_robot_audio(self):
        """Check if robot audio is available."""
        if self.reachy_mini is None:
            return False
        if hasattr(self.reachy_mini, 'media'):
            try:
                if hasattr(self.reachy_mini.media, 'play_sound'):
                    return True
            except:
                pass
        return False

    def play_jingle_bells(self):
        """Play wake up sound on robot."""
        if not self._lock.acquire(blocking=False):
            return  # Already playing
        
        try:
            if self._can_use_robot_audio():
                print("[Sound] 🎶 Playing wake_up on robot... 🎶")
                try:
                    self.reachy_mini.media.play_sound("wake_up.wav")
                except Exception as e:
                    print(f"[Sound] Robot audio error: {e}")
            else:
                print("[Sound] 🎶 Jingle Bells (robot not connected) 🎶")
        finally:
            self._lock.release()

    def play_surprise(self):
        """Play surprise/alert sound on robot."""
        self._lock.acquire(timeout=0.5)
        
        try:
            if self._can_use_robot_audio():
                print("[Sound] ❗ SURPRISE on robot! ❗")
                try:
                    self.reachy_mini.media.play_sound("go_sleep.wav")
                except Exception as e:
                    print(f"[Sound] Robot audio error: {e}")
            else:
                print("[Sound] ❗ SURPRISE (robot not connected) ❗")
        finally:
            if self._lock.locked():
                self._lock.release()

    def stop(self):
        """Stop placeholder."""
        pass


# Global instance (will get reachy set later)
sound_player = SoundGenerator()
