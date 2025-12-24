"""Vision system that uses Reachy Mini's built-in camera for face detection."""

import threading
import time

# Try to import OpenCV for face detection
try:
    import cv2
    from pathlib import Path
    
    # Use bundled asset if available
    bundled_cascade = Path(__file__).parent / "assets" / "haarcascade_frontalface_default.xml"
    if bundled_cascade.exists():
        cascade_path = str(bundled_cascade)
    else:
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        
    FACE_CASCADE = cv2.CascadeClassifier(cascade_path)
    if FACE_CASCADE.empty():
        raise ValueError('Failed to load Haar cascade')
    HAS_OPENCV = True
except Exception as e:
    HAS_OPENCV = False
    FACE_CASCADE = None
    print(f"Warning: OpenCV not available. Face detection disabled. Error: {e}")


class VisionSystem:
    """Vision system using Reachy Mini's camera for face detection."""

    def __init__(self, reachy_mini=None):
        self.reachy_mini = reachy_mini
        self.running = False
        self.face_detected = False
        self._thread = None
        self._lock = threading.Lock()

    def start(self):
        """Start the vision processing loop."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the vision processing loop."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def _loop(self):
        """Main vision processing loop."""
        # Log camera status
        if self.reachy_mini is None:
            print("[Vision] No robot instance - running in mock mode")
        elif self.reachy_mini.media is None:
            print("[Vision] No media manager - running in mock mode")
        elif self.reachy_mini.media.camera is None:
            print("[Vision] Camera is None - will try get_frame() anyway")
        else:
            print("[Vision] Camera available")
        
        print(f"[Vision] OpenCV available: {HAS_OPENCV}")
        
        # Can we try to get frames?
        can_try_camera = (
            self.reachy_mini is not None 
            and self.reachy_mini.media is not None 
            and HAS_OPENCV
        )
        
        if can_try_camera:
            print("[Vision] Will attempt face detection via get_frame()")
        else:
            print("[Vision] Running in mock mode - face_detected always False")
        
        while self.running:
            if can_try_camera:
                try:
                    frame = self.reachy_mini.media.get_frame()
                    
                    if frame is not None:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        faces = FACE_CASCADE.detectMultiScale(
                            gray,
                            scaleFactor=1.1,
                            minNeighbors=5,
                            minSize=(30, 30)
                        )
                        with self._lock:
                            self.face_detected = len(faces) > 0
                    else:
                        with self._lock:
                            self.face_detected = False
                            
                except Exception as e:
                    print(f"[Vision] Error: {e}")
                    with self._lock:
                        self.face_detected = False
                
                time.sleep(0.05)  # ~20 FPS
            else:
                with self._lock:
                    self.face_detected = False
                time.sleep(0.5)

    def is_face_present(self):
        """Return whether a face is currently detected."""
        with self._lock:
            return self.face_detected
            
    @property
    def status(self) -> str:
        """Return current status."""
        if not HAS_OPENCV:
            return 'no_opencv'
        if self.reachy_mini is None:
            return 'mock'
        return 'ok'

    def get_faces(self):
        """Return a list of detected faces."""
        with self._lock:
            if self.face_detected:
                return [{"bbox": [0, 0, 1, 1]}]
            return []

