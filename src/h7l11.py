import time
from hx711 import HX711

DT_PIN = 29
SCK_PIN = 31

hx = HX711(DT_PIN, SCK_PIN)

hx.set_scale(2280)  
hx.tare()  

print("Balanza lista. Coloca el objeto para medir.")
try:
    while True:
        peso = hx.get_grams()
        print(f"Peso: {peso:.2f} gramos")
        time.sleep(1)
except KeyboardInterrupt:
    print("Saliendo del programa...")
finally:
    hx.cleanup()
