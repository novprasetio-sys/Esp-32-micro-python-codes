import network
import urequests
import time
from machine import Pin

# =========================
# WIFI
# =========================
SSID = "WIFI"
PASSWORD = "PASSWORD"

# =========================
# TELEGRAM
# =========================
BOT_TOKEN = "TOKEN"
CHAT_ID = "CHAT_ID"

URL = "https://api.telegram.org/bot"+BOT_TOKEN+"/sendMessage"

# =========================
# INPUT OVERLOAD
# =========================
overload = Pin(15, Pin.IN, Pin.PULL_UP)

last_state = overload.value()

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

# =========================
# MAIN LOOP
# =========================
while True:

    # reconnect wifi jika putus
    if not wlan.isconnected():

        wlan = connect_wifi()

    state = overload.value()

    if state != last_state:

        time.sleep(0.2)   # debounce

        state = overload.value()

        if state == 0:

            send_telegram("⚠️ OVERLOAD TRIP")

        else:

            send_telegram("✅ OVERLOAD NORMAL")

        last_state = state

    time.sleep(0.5)
