from hx711 import HX711
import RPi.GPIO as GPIO
import time

def setup_hx711():
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

def read_weight(hx):
    try:
        raw_weight = hx.get_raw_data_mean()

        reference_unit = 1 
        weight = (raw_weight - hx.offset) / reference_unit if raw_weight is not None else None

        return weight
    except Exception as e:
        print(f"Error al leer el peso: {e}")
        return None

def main():
    """Función principal para leer pesos continuamente."""
    GPIO.setmode(GPIO.BOARD)

    hx = setup_hx711()

    try:
        while True:
            weight = read_weight(hx)
            if weight is not None:
                print(f"Peso: {weight:.2f} gramos")
            else:
                print("Error al obtener el peso.")

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSaliendo del programa...")
    finally:
        hx.power_down()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
