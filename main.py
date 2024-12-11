import cv2
import numpy as np
import os
import time

def main():
    
    capture_folder = "capturas"
    os.makedirs(capture_folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se puede acceder a la cámara")
        return

    model_cfg = 'yolov3.cfg' 
    model_weights = 'yolov3.weights'  
    labels_path = 'coco.names'  

    with open(labels_path, 'r') as f:
        classes = f.read().strip().split('\n')

    net = cv2.dnn.readNetFromDarknet(model_cfg, model_weights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

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

        height, width, _ = frame.shape

        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(output_layers)

        boxes = []
        confidences = []
        class_ids = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5: 
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        detection_made = False 

        if len(indices) > 0: 
            if isinstance(indices, np.ndarray):  
                for i in indices.flatten():
                    x, y, w, h = boxes[i]
                    label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
                    color = (0, 255, 0)  # Verde
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    detection_made = True
            elif isinstance(indices, (int, np.integer)):
                i = indices
                x, y, w, h = boxes[i]
                label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
                color = (0, 255, 0)  # Verde
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
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