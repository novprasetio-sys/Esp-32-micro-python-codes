from machine import Pin
import time
# Pin sensor IR
IR = Pin(35, Pin.IN)
# Pin Aktuator
POMPA = Pin(2, Pin.OUT)
while True:
    # membaca nilai logic
    high_level = IR.value()
    # logika bersyarat nilai logic
    if high_level == 1 :
        POMPA.value(1) 
    else :
        POMPA.value(0) 
    print("High Level:", high_level, "Pompa:", POMPA.value())
    time.sleep(0.1)