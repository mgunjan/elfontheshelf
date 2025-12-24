"""Audio generator that plays sounds on Reachy Mini robot."""

import threading


class SoundGenerator:
    """Sound generator using Reachy Mini's built-in sounds."""
    
    def __init__(self, reachy_mini=None):
        self.reachy_mini = reachy_mini
        self._lock = threading.Lock()

    def set_reachy(self, reachy_mini):
        """Set the ReachyMini instance."""
        self.reachy_mini = reachy_mini
        # Log media backend for debugging
        if hasattr(reachy_mini, 'media_manager'):
            print(f"[Sound] Media backend: {reachy_mini.media_manager.backend}")
        if reachy_mini.media is not None:
            print(f"[Sound] Audio initialized: {reachy_mini.media.audio is not None}")

    def play_jingle_bells(self):
        """Play jingle.wav sound on robot."""
        if self.reachy_mini is None:
            return
        if not self._lock.acquire(blocking=False):
            return
        
        try:
            print("[Sound] 🎶 Playing jingle.wav...")
            self.reachy_mini.media.play_sound("jingle.wav")
        except Exception as e:
            print(f"[Sound] Error: {e}")
        finally:
            self._lock.release()

    def play_surprise(self):
        """Play surprise.wav sound on robot."""
        if self.reachy_mini is None:
            return
        if not self._lock.acquire(blocking=False):
            return
        
        try:
            print("[Sound] ❗ Playing surprise.wav...")
            self.reachy_mini.media.play_sound("surprise.wav")
        except Exception as e:
            print(f"[Sound] Error: {e}")
        finally:
            self._lock.release()

    def stop(self):
        pass


# Global instance
sound_player = SoundGenerator()

