import cv2
import numpy as np
import os
import time
from ultralytics import YOLO

def main():

    capture_folder = "capturas"
    os.makedirs(capture_folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se puede acceder a la cámara")
        return

    model_path = os.path.join('yolo_cuy_model.pt')
    model = YOLO(model_path)

    classes = ['cuy']  

    cv2.namedWindow('Cámara en tiempo real', cv2.WINDOW_NORMAL)
    print("Presiona 'q' para salir")

    frame_counter = 0
    last_capture_time = 0
    capture_interval = 3 

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el frame")
            break

        results = model.predict(frame, conf=0.25)

        detection_made = False
        for result in results:
        
            boxes = result.boxes.xyxy 
            confidences = result.boxes.conf 
            class_ids = result.boxes.cls 

            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = box
                confidence = confidences[i]
                class_id = int(class_ids[i])

                if confidence > 0.5: 
                    label = f"{classes[class_id]}: {confidence:.2f}"
                    color = (0, 255, 0)  

                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    detection_made = True

        current_time = time.time()
        if detection_made and (current_time - last_capture_time >= capture_interval):
            frame_counter += 1
            filename = os.path.join(capture_folder, f"captura_{frame_counter}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Captura guardada: {filename}")
            last_capture_time = current_time

        cv2.imshow('Cámara en tiempo real', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
