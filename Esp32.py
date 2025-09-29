import network
import time
import machine
import socket

LED_POWER = machine.Pin(2, machine.Pin.OUT)
LED_WIFI = machine.Pin(15, machine.Pin.OUT)

# Change these values according to your network name (SSID) and password
SSID = "Daniki Helix"
PASSWORD = "1811TheCatTheFox"

LED_POWER.value(1)  # Board is powered on

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Blinking while connecting
blink = True
while not wlan.isconnected():
    LED_WIFI.value(blink)
    blink = not blink
    time.sleep(0.5)
    wlan.connect(SSID, PASSWORD)

# Connected, turn WiFi LED ON
LED_WIFI.value(1)
print("Connected to WiFi:", wlan.ifconfig())

#a tiny web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

#define the response to all requests
html_response = b"""\
HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n
<html>
  <body>
    <h2>Hello from ESP32!</h2>
  </body>
</html>
"""
#always wait fo requests and respond with the above response
while True:
    #accept the incoming connection
    cl, addr = s.accept()
    print('Client connected from', addr)
    # Read, display, and discard all headers (We must completely receive the request to ensure consistent behaviour)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        print(line)
        if not line or line == b"\r\n":
            break
    #now send the response to the client
    cl.send(html_response)
    #close the connection
    cl.close()
    print('Response sent to client at', addr)
