import threading
import time
from hx711 import HX711
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class WeightService:
    def __init__(self, capture_event, threshold=50):
        self.capture_event = capture_event
        self.threshold = threshold
        self.hx = self.setup_hx711()

    def setup_hx711(self):
        hx = HX711(dout_pin=29, pd_sck_pin=31)
        hx.reset()

        print("Realizando tara, por favor no coloque peso en la balanza...")
        time.sleep(2)
        tara_value = hx.get_raw_data_mean()
        if tara_value is not None:
            hx.offset = tara_value
            print(f"Tara completada, offset establecido en: {hx.offset}")
        else:
            print("Error al realizar la tara. Verifique las conexiones.")

        print("HX711 configurado y tarado. Listo para leer.")
        return hx

    def read_weight(self):
        try:
            raw_weight = self.hx.get_raw_data_mean()
            reference_unit = 1  # Configura según tu calibración
            weight = (raw_weight - self.hx.offset) / reference_unit if raw_weight is not None else None
            return weight
        except Exception as e:
            print(f"Error al leer el peso: {e}")
            return None

    def start(self):
        try:
            while True:
                weight = self.read_weight()
                if weight and weight > self.threshold:
                    print(f"Peso detectado: {weight}g")
                    self.capture_event.set()  # Activa el evento para captura de imagen
                time.sleep(1)
        except KeyboardInterrupt:
            print("Saliendo del servicio de peso...")
        finally:
            self.hx.power_down()
            GPIO.cleanup()