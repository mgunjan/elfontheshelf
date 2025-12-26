"""Audio generator that plays sounds on Reachy Mini robot."""

import threading
import os
from pathlib import Path


class SoundGenerator:
    """Sound generator using bundled assets with SDK fallback."""
    
    def __init__(self, reachy_mini=None):
        self.reachy_mini = reachy_mini
        self._lock = threading.Lock()
        
        # Resolve asset paths using multiple strategies
        self.jingle_path = self._find_asset("jingle.wav")
        self.surprise_path = self._find_asset("surprise.wav")
        
    def _find_asset(self, filename):
        """Find an asset file using multiple strategies."""
        candidates = [
            # 1. Relative to this file (best for installed package)
            Path(__file__).parent / "assets" / filename,
            # 2. Relative to current working directory
            Path(os.getcwd()) / "elf_on_shelf" / "assets" / filename,
            Path(os.getcwd()) / "assets" / filename,
            # 3. Look in reachable site-packages (hacky but effective)
            Path(__file__).parent.parent / "elf_on_shelf" / "assets" / filename,
        ]
        
        for cand in candidates:
            if cand.exists():
                print(f"[Sound] Found {filename} at: {cand}")
                return cand
                
        # 4. If all else fails, use a recursive search in the parent directory
        # (This handles weird install structures)
        try:
            parent = Path(__file__).parent.parent
            for path in parent.rglob(filename):
                print(f"[Sound] Found {filename} via glob at: {path}")
                return path
        except Exception:
            pass
            
        print(f"[Sound] ❌ Could not find {filename}!")
        return Path(filename) # Return bare path as last resort

    def set_reachy(self, reachy_mini):
        """Set the ReachyMini instance."""
        self.reachy_mini = reachy_mini
        if hasattr(reachy_mini, 'media_manager'):
            print(f"[Sound] Media backend: {reachy_mini.media_manager.backend}")

    def play_jingle_bells(self):
        """Play jingle.wav if available, else wake_up.wav."""
        if self.reachy_mini is None:
            return
        if not self._lock.acquire(blocking=False):
            return
        
        try:
            if self.jingle_path.exists():
                print(f"[Sound] 🎶 Playing {self.jingle_path.name}...")
                self.reachy_mini.media.play_sound(str(self.jingle_path))
            else:
                print("[Sound] 🎶 Playing wake_up.wav (fallback)...")
                self.reachy_mini.media.play_sound("wake_up.wav")
        except Exception as e:
            print(f"[Sound] Error: {e}")
        finally:
            self._lock.release()

    def play_surprise(self):
        """Play surprise.wav if available, else go_sleep.wav."""
        if self.reachy_mini is None:
            return
        if not self._lock.acquire(blocking=False):
            return
        
        try:
            if self.surprise_path.exists():
                print(f"[Sound] ❗ Playing {self.surprise_path.name}...")
                self.reachy_mini.media.play_sound(str(self.surprise_path))
            else:
                print("[Sound] ❗ Playing go_sleep.wav (fallback)...")
                self.reachy_mini.media.play_sound("go_sleep.wav")
        except Exception as e:
            print(f"[Sound] Error: {e}")
        finally:
            self._lock.release()

    def stop(self):
        pass


# Global instance
sound_player = SoundGenerator()
