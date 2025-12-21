from machine import Pin, time_pulse_us
import utime
import time
# Ultrasonic pins 
TRIG = Pin(4, Pin.OUT)
ECHO = Pin(34, Pin.IN)
buzzer = Pin(2, Pin.OUT)
def get_distance():
    TRIG.value(1)
    utime.sleep_us(5)
    TRIG.value(0)
    utime.sleep_us(10)
    TRIG.value(0)
    # fungsi pembacaan jarak
    duration = time_pulse_us(ECHO, 1, 30000)
    distance = (duration / 2) / 29.1
    return distance
while True:
    d = get_distance()
    print(d)
    # logika bersyarat jarak
    if d <= 5:
        buzzer.value(1)
    else:
        buzzer.value(0)
    time.sleep(0.1)