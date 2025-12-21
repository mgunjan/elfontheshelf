import math
import time
import threading
import random
import sys
import os

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False

class SoundGenerator:
    def __init__(self):
        self.rate = 44100
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.current_thread = None

    def generate_tone(self, frequency, duration, volume=0.5):
        if not HAS_NUMPY: return np.array([], dtype=np.float32)
        
        # Determine number of samples
        n_samples = int(self.rate * duration)
        
        # Generate sine wave
        t = np.linspace(0, duration, n_samples, False)
        # 8-bit style simulation (keeping it simple sine for now, but could clip)
        wave = np.sin(frequency * t * 2 * np.pi)
        
        # Envelope to de-click
        fade_len = min(int(self.rate * 0.05), n_samples // 2)
        
        envelope = np.concatenate([
            np.linspace(0, 1, fade_len),
            np.ones(n_samples - 2 * fade_len),
            np.linspace(1, 0, fade_len)
        ])
        if len(envelope) > len(wave): envelope = envelope[:len(wave)]
        if len(wave) > len(envelope): wave = wave[:len(envelope)]
        
        wave = wave * envelope * volume
        return wave.astype(np.float32)

    def play_jingle_bells(self):
        # Ensure only one song plays at a time
        if not self._lock.acquire(blocking=False):
            return # Already playing something
            
        if not HAS_SOUNDDEVICE or not HAS_NUMPY:
            print("[Sound] Playing Jingle Bells (Mock)")
            self._lock.release()
            time.sleep(2)
            return
            
        print("[Sound] 🎶 Playing Jingle Bells... 🎶")
        self.current_thread = threading.current_thread()

        notes = [
            (329.63, 0.3), (329.63, 0.3), (329.63, 0.6),
            (0, 0.1),
            (329.63, 0.3), (329.63, 0.3), (329.63, 0.6),
            (0, 0.1),
            (329.63, 0.3), (392.00, 0.3), (261.63, 0.4), (293.66, 0.2), (329.63, 0.8)
        ]

        try:
            # Prepare full buffer or stream? Streaming is better for interrupt.
            with sd.OutputStream(samplerate=self.rate, channels=1, dtype='float32') as stream:
                for freq, dur in notes:
                    if self._stop_event.is_set(): 
                        break
                    
                    if freq == 0:
                        time.sleep(dur)
                    else:
                        audio_data = self.generate_tone(freq, dur)
                        # instant play? stream.write blocks until consumed
                        stream.write(audio_data)
        except Exception as e:
             print(f"[Sound] Jingle interrupted or error: {e}")
        finally:
            self._lock.release()
            self._stop_event.clear()

    def play_surprise(self):
        """Play a dramatic '!] Alert' style sound. Interrupts everything."""
        self._stop_event.set()
        
        # Wait briefly for lock
        self._lock.acquire(timeout=0.5) 
        
        if not HAS_SOUNDDEVICE or not HAS_NUMPY:
            print("[Sound] ❗ SURPRISE! ❗")
            if self._lock.locked(): self._lock.release()
            return

        print("[Sound] ❗ SURPRISE! ❗")
        try:
             # Generate Full Sequence
            full_audio = np.array([], dtype=np.float32)
            
            # 1. Hit
            full_audio = np.concatenate([full_audio, self.generate_tone(1500, 0.05, volume=0.9)])
             # 2. Slide
            for f in range(1200, 400, -80):
                full_audio = np.concatenate([full_audio, self.generate_tone(f, 0.02, volume=0.7)])

            sd.play(full_audio, self.rate, blocking=True)
            
        except Exception as e:
            print(f"[Sound] Error playing surprise: {e}")
        finally:
            if self._lock.locked():
                self._lock.release()
            self._stop_event.clear()

    def stop(self):
        self._stop_event.set()
        sd.stop()

sound_player = SoundGenerator()
