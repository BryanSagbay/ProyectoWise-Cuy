import os
import time
import cv2
from ultralytics import YOLO

class ImageCaptureService:
    def __init__(self, capture_event, capture_folder="capturas", model_path="models/cuy_model.pt"):
        self.capture_event = capture_event
        self.capture_folder = capture_folder
        os.makedirs(self.capture_folder, exist_ok=True)
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise RuntimeError("No se puede acceder a la cámara")

    def capture_image(self):
        ret, frame = self.cap.read()
        if not ret:
            print("No se pudo capturar el frame")
            return None
        return frame

    def process_detections(self, frame):
        results = self.model.predict(frame, conf=0.25)
        detections = []
        for result in results:
            for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls):
                if conf > 0.5:
                    detections.append({
                        "bbox": box.tolist(),
                        "confidence": float(conf),
                        "class_id": int(cls)
                    })
        return detections

    def save_image(self, frame, detections):
        timestamp = int(time.time())
        filename = os.path.join(self.capture_folder, f"captura_{timestamp}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Imagen guardada: {filename}")
        return filename

    def start(self):
        try:
            while True:
                self.capture_event.wait()  
                self.capture_event.clear() 

                frame = self.capture_image()
                if frame is not None:
                    detections = self.process_detections(frame)
                    if detections:
                        self.save_image(frame, detections)
        except KeyboardInterrupt:
            print("Saliendo del servicio de captura de imágenes...")
        finally:
            self.cap.release()
            cv2.destroyAllWindows()