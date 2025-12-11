import network
import socket
import time
from machine import Pin, time_pulse_us

# ------------------------------
# Setup Ultrasound HC-SR04
# ------------------------------
TRIG = Pin(5, Pin.OUT)
ECHO = Pin(18, Pin.IN)

def read_distance():
    TRIG.off()
    time.sleep_us(5)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()

    duration = time_pulse_us(ECHO, 1, 30000)  # timeout 30ms
    if duration <= 0:
        return -1

    distance = (duration * 0.0343) / 2
    return round(distance, 2)

# ------------------------------
# Setup Access Point
# ------------------------------
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP32_ULTRA_AP", password="12345678")
print("AP IP:", ap.ifconfig()[0])

# ------------------------------
# Simple Web Server
# ------------------------------
html = """<!DOCTYPE html>
<html>
<head>
<title>Ultrasonic ESP32</title>
<meta http-equiv='refresh' content='1'>
<style>
body { font-family: Arial; text-align: center; margin-top: 40px; }
.card {
    display: inline-block;
    padding: 20px 40px;
    border-radius: 12px;
    background: #f2f2f2;
    font-size: 24px;
}
</style>
</head>
<body>
<h2>ESP32 Ultrasonic Web Server</h2>
<div class='card'>
Distance: <b>{DIST} cm</b>
</div>
</body>
</html>
"""

# Start socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 80))
sock.listen(5)
print("Web Server Running...")

while True:
    conn, addr = sock.accept()
    print("Client connected:", addr)

    request = conn.recv(1024)

    distance = read_distance()
    if distance == -1:
        dist_text = "No Echo"
    else:
        dist_text = str(distance)

    response = html.replace("{DIST}", dist_text)
    conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    conn.send(response)
    conn.close()