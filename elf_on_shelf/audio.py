import struct
import threading
import time
import os

try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False
    print("Warning: PyAudio not found. AudioSystem will be mocked.")

try:
    import pvporcupine
    HAS_PORCUPINE = True
except ImportError:
    HAS_PORCUPINE = False

class AudioSystem:
    def __init__(self, access_key=None, keyword_paths=None, sensitivity=0.5):
        self.access_key = access_key
        self.keyword_paths = keyword_paths
        self.sensitivity = sensitivity
        self.running = False
        self.triggered = False
        self._thread = None
        self.porcupine = None
        self.pa = None
        self.audio_stream = None

    def start(self):
        if self.running:
            return

        if HAS_PORCUPINE and self.access_key:
            try:
                self.porcupine = pvporcupine.create(
                    access_key=self.access_key,
                    keyword_paths=self.keyword_paths,
                    sensitivities=[self.sensitivity] * len(self.keyword_paths) if self.keyword_paths else [self.sensitivity]
                )
            except Exception as e:
                print(f"Failed to initialize Porcupine: {e}")
                self.porcupine = None
        
        if HAS_PYAUDIO:
            self.pa = pyaudio.PyAudio()
            if self.porcupine:
                self.audio_stream = self.pa.open(
                    rate=self.porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=self.porcupine.frame_length
                )
            else:
                # Fallback mock stream
                self.audio_stream = self.pa.open(
                    rate=16000,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=512
                )
        else:
            self.pa = None
            self.audio_stream = None

        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join()
        
        if self.audio_stream:
            self.audio_stream.close()
        if self.pa:
            self.pa.terminate()
        if self.porcupine:
            self.porcupine.delete()

    def _loop(self):
        while self.running:
            if self.porcupine:
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    self.triggered = True
            else:
                # Mock behavior: Simple energy detection or random logic could go here
                # For now, we wait for a manual override or just sleep
                time.sleep(0.1)
                
            # Reset trigger is handled by the consumer usually, 
            # or we convert this to an event queue. 
            # For this simple app, we keep 'triggered' true until consumed.

    def is_triggered(self):
        if self.triggered:
            self.triggered = False
            return True
        return False
