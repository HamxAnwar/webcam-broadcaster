import cv2
import logging
import threading

class Camera:
    def __init__(self, camera_index=0):
        """
        Initialize the camera.
        
        Args:
            camera_index: Index of the camera device (default: 0)
        """
        self.camera_index = camera_index
        self.camera = None
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        
    def start(self):
        """Start the camera capture."""
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            if not self.camera.isOpened():
                self.logger.error(f"Failed to open camera at index {self.camera_index}")
                return False
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.logger.info(f"Camera started at index {self.camera_index}")
            return True
        except Exception as e:
            self.logger.error(f"Error starting camera: {e}")
            return False
    
    def get_frame(self):
        """
        Get a frame from the camera.
        
        Returns:
            bytes: JPEG encoded frame, or None if frame not available
        """
        with self.lock:
            if self.camera is None or not self.camera.isOpened():
                return None
            
            try:
                success, frame = self.camera.read()
                if not success:
                    return None
                
                # Encode frame as JPEG
                ret, buffer = cv2.imencode('.jpg', frame, 
                                           [int(cv2.IMWRITE_JPEG_QUALITY), 85])
                if ret:
                    return buffer.tobytes()
                return None
            except Exception as e:
                self.logger.error(f"Error getting frame: {e}")
                return None
    
    def stop(self):
        """Stop the camera capture."""
        with self.lock:
            if self.camera is not None:
                self.camera.release()
                self.camera = None
                self.logger.info("Camera stopped")
    
    def is_running(self):
        """Check if the camera is running."""
        return self.camera is not None and self.camera.isOpened()
    
    def get_info(self):
        """Get camera information."""
        if self.camera is None:
            return {"status": "not_initialized"}
        
        if not self.camera.isOpened():
            return {"status": "not_opened"}
        
        return {
            "status": "running",
            "width": int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": int(self.camera.get(cv2.CAP_PROP_FPS)),
            "camera_index": self.camera_index
        }
