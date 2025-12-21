import threading
import time

try:
    import cv2
    import mediapipe as mp
    # Verify critical submodules to avoid later crashes
    if not hasattr(mp, 'solutions'):
        raise ImportError("mediapipe.solutions missing")
    import numpy as np
    HAS_VISION_LIBS = True
except (ImportError, AttributeError):
    HAS_VISION_LIBS = False
    print("Warning: Vision libraries (opencv, mediapipe) not found or broken. VisionSystem will be mocked.")

class VisionSystem:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.running = False
        self.face_detected = False
        self._thread = None
        self.cap = None
        
        if HAS_VISION_LIBS:
            self.face_detection = mp.solutions.face_detection.FaceDetection(
                model_selection=0, min_detection_confidence=0.5
            )
        else:
            self.face_detection = None

    def start(self):
        if self.running:
            return
        
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join()
        if self.cap:
            self.cap.release()

    def _loop(self):
        if HAS_VISION_LIBS:
            self.cap = cv2.VideoCapture(self.camera_index)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while self.running:
            if HAS_VISION_LIBS:
                success, image = self.cap.read()
                if not success:
                    time.sleep(0.1)
                    continue

                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = self.face_detection.process(image)

                if results.detections:
                    self.face_detected = True
                else:
                    # Mock logic for testing: trigger face occasionally if needed
                    # self.face_detected = False
                    self.face_detected = False
                
                time.sleep(0.05)
            else:
                # Mock Loop
                # "Peekaboo Mode": Toggle face detected every 10 seconds to let users test Surprise Mode
                now = time.time()
                # 10s cycle: 0-5s = No Face (Alive), 5-10s = Face (Surprise/Freeze)
                if (now % 20) > 10: 
                     # 10 seconds of "Face Detected"
                     if not self.face_detected:
                        # Log only on edge
                        # print("[MockVision] Peekaboo! Face Detected (Testing Surprise Mode)")
                        pass
                     self.face_detected = True
                else:
                     # 10 seconds of "No Face"
                     if self.face_detected:
                        # print("[MockVision] Face Gone (Testing Alive Mode)")
                        pass
                     self.face_detected = False
                
                time.sleep(0.1)


    def is_face_present(self):
        return self.face_detected

    def get_faces(self):
        """Returns a list of detected faces (mocks logic for MagicMode compatibility)."""
        if self.face_detected:
            return [{"bbox": [0,0,1,1]}] # fast dummy response
        return []
