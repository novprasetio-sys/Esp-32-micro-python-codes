import network
import urequests
import time
from machine import Pin

# Konfigurasi WiFi
SSID = "nama_wifi"
PASSWORD = "password_wifi"

# Konfigurasi Telegram
TELEGRAM_TOKEN = "token_bot_telegram"
TELEGRAM_CHAT_ID = "chat_id_telegram"

# Inisialisasi pin sensor PIR
pir = Pin(25, Pin.IN)

# Inisialisasi WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Menghubungkan ke WiFi...")
    time.sleep(1)

print("Terhubung ke WiFi")

def kirim_pesan_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    headers = {"Content-Type": "application/json"}
    data = '{"chat_id": "' + TELEGRAM_CHAT_ID + '", "text": "' + pesan + '"}'
    response = urequests.post(url, headers=headers, data=data)
    print(response.text)

status_sebelumnya = 0

while True:
    # Baca status sensor PIR
    status_sekarang = pir.value()
    if status_sekarang != status_sebelumnya:
        if status_sekarang == 1:
            print("Gerakan terdeteksi")
            kirim_pesan_telegram("Gerakan terdeteksi")
        else:
            print("Tidak ada gerakan")
            kirim_pesan_telegram("Tidak ada gerakan")
        status_sebelumnya = status_sekarang
    
    time.sleep(1)
