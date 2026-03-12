import time
from machine import Pin

ldr = Pin(25, Pin.IN)
led = Pin(2, Pin.OUT)

while True:
    # Baca status sensor PIR
    status_sekarang = ldr.value()
    if status_sekarang == 0:
        led.value(1)
        print(status_sekarang)
        print("api terdeteksi")           
    else:
        led.value(0)
        print(status_sekarang)
        print("aman")
    time.sleep(1)
