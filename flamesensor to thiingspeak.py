import network
import urequests
import time
from machine import Pin

# =========================
# WIFI
# =========================
SSID = "xxxxxxx"
PASSWORD = "xxxxxxx"

# =========================
# TELEGRAM
# =========================
BOT_TOKEN = "xxxxxx"
CHAT_ID = "xxxxxxx"

URL = "https://api.telegram.org/bot"+BOT_TOKEN+"/sendMessage"

ldr = Pin(25, Pin.IN)
led = Pin(2, Pin.OUT)

last_state = ldr.value()

# =========================
# WIFI CONNECT FUNCTION
# =========================
def connect_wifi():

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():

        print("Connecting WiFi...")

        wlan.connect(SSID, PASSWORD)

        while not wlan.isconnected():
            time.sleep(1)

    print("WiFi Connected")

    return wlan


wlan = connect_wifi()

# =========================
# TELEGRAM SEND FUNCTION
# =========================
def send_telegram(msg):

    try:

        url = URL + "?chat_id=" + CHAT_ID + "&text=" + msg
        r = urequests.get(url)
        r.close()

        print("Telegram:", msg)

    except:

        print("Telegram send error")


# =========================
# START MESSAGE
# =========================
send_telegram("📡 ESP32 Monitoring Start")

while True:
    # Baca status sensor PIR
    status_sekarang = ldr.value()
     # reconnect wifi jika putus
    if not wlan.isconnected():

        wlan = connect_wifi()
        
    state = ldr.value()
    
    if state != last_state:

        time.sleep(0.2)   # debounce

        state = ldr.value()


        if status_sekarang == 0:

            send_telegram("⚠️ danger fire detected ")

        else:

            send_telegram("✅ aman")
            
        last_state = state


    time.sleep(0.5)
