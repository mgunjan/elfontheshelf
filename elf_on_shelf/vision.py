"""Vision system that uses Reachy Mini's built-in camera for face detection."""

import threading
import time

# Try to import OpenCV for face detection
try:
    import cv2
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
        """Initialize vision system.
        
        Args:
            reachy_mini: ReachyMini instance to get camera frames from.
                        If None, runs in mock mode (no face detection).
        """
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
        # Check if camera is available (not no_media mode)
        has_camera = False
        if self.reachy_mini is not None and hasattr(self.reachy_mini, 'media'):
            try:
                # Check if media manager has a camera
                if hasattr(self.reachy_mini.media, 'camera') and self.reachy_mini.media.camera is not None:
                    has_camera = True
            except:
                pass
        
        if has_camera and HAS_OPENCV:
            print("[Vision] Using robot camera for face detection")
        else:
            print("[Vision] Running in mock mode (no camera) - defaulting to Alive behavior")
        
        while self.running:
            # Check if we have a real robot connection with camera
            if has_camera and HAS_OPENCV:
                try:
                    # Get frame from robot's camera
                    frame = self.reachy_mini.media.get_frame()
                    
                    if frame is not None:
                        # Convert to grayscale for face detection
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        
                        # Detect faces using Haar cascade
                        faces = FACE_CASCADE.detectMultiScale(
                            gray,
                            scaleFactor=1.1,
                            minNeighbors=5,
                            minSize=(30, 30)
                        )
                        
                        with self._lock:
                            self.face_detected = len(faces) > 0
                    else:
                        # No frame available
                        with self._lock:
                            self.face_detected = False
                            
                except Exception as e:
                    # Camera error - default to no face
                    print(f"[Vision] Camera error: {e}")
                    with self._lock:
                        self.face_detected = False
                
                time.sleep(0.05)  # ~20 FPS
            else:
                # Mock mode: no robot camera or no OpenCV
                # Default to NO FACE (Alive Mode) so Jingle Bells can play
                with self._lock:
                    self.face_detected = False
                time.sleep(0.5)

    def is_face_present(self):
        """Return whether a face is currently detected."""
        with self._lock:
            return self.face_detected

    def get_faces(self):
        """Return a list of detected faces for MagicMode compatibility."""
        with self._lock:
            if self.face_detected:
                return [{"bbox": [0, 0, 1, 1]}]  # Dummy bbox
            return []
