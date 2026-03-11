from machine import Pin
import time

# Inisialisasi pin sensor PIR
pir = Pin(25, Pin.IN)

def gerakan_terdeteksi(pin):
    if pir.value() == 1:
        print("Gerakan terdeteksi")
    else:
        print("Tidak ada gerakan")

pir.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=gerakan_terdeteksi)

while True:
    time.sleep(1)
