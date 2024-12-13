import threading
import time
from services.weight_service import WeightService
from services.objdetection_service import ImageCaptureService

def main():
    capture_event = threading.Event()

    weight_service = WeightService(capture_event)
    image_service = ImageCaptureService(capture_event)

    threading.Thread(target=weight_service.start, daemon=True).start()
    threading.Thread(target=image_service.start, daemon=True).start()

    print("Servicios iniciados. Presiona Ctrl+C para salir.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Cerrando aplicación principal...")

if __name__ == "__main__":
    main()