import network
import time
import machine
import socket

# LED setup
LED_POWER = machine.Pin(2, machine.Pin.OUT)
LED_WIFI = machine.Pin(15, machine.Pin.OUT)

SSID = "name"
PASSWORD = "password"

LED_POWER.value(1)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    LED_WIFI.value(0)
    time.sleep(0.5)
    LED_WIFI.value(1)
    time.sleep(0.5)

LED_WIFI.value(1)
print("Connected to WiFi:", wlan.ifconfig())

# Start server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

# Define different pages
page_index = b"""\
HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n
<html><body><h2>Welcome to the ESP32 Web Server!</h2></body></html>
"""

page_about = b"""\
HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n
<html><body><h2>About Page</h2><p>This ESP32 is running MicroPython.</p></body></html>
"""

page_not_found = b"""\
HTTP/1.0 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n
<html><body><h2>404 Page Not Found</h2></body></html>
"""

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)  # get the request data
    request_str = request.decode()
    print("Request:", request_str)

    # Look at the first line of the request
    if "GET / " in request_str:
        response = page_index
    elif "GET /about" in request_str:
        response = page_about
    else:
        response = page_not_found

    cl.send(response)
    cl.close()
