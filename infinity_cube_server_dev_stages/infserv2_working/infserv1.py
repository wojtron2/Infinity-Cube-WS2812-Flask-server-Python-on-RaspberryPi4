from flask import Flask, request, jsonify, send_from_directory
from rpi_ws281x import Adafruit_NeoPixel, Color

app = Flask(__name__, static_folder='static')

# Konfiguracja LED
LED_COUNT      = 237
LED_PIN        = 18
LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 25  # Domyślna jasność
LED_INVERT     = False
LED_CHANNEL    = 0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def set_color(strip, color):
    """Ustawienie koloru na wszystkich diodach"""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/set_color', methods=['GET'])
def change_color():
    r = int(request.args.get('r', 0))
    g = int(request.args.get('g', 0))
    b = int(request.args.get('b', 0))
    set_color(strip, Color(r, g, b))
    return jsonify({'status': 'OK', 'color': (r, g, b)})

@app.route('/set_brightness', methods=['GET'])
def set_brightness():
    global strip
    brightness = int(request.args.get('brightness', 25))
    brightness = max(0, min(255, brightness))  # Ograniczenie do zakresu 0-255

    # Zmiana jasnosci i ponowne uruchomienie paska LED
    strip.setBrightness(brightness)
    strip.show()
    return jsonify({'status': 'OK', 'brightness': brightness})

@app.route('/off', methods=['GET'])
def turn_off():
    set_color(strip, Color(0, 0, 0))
    return jsonify({'status': 'OFF'})

if __name__ == '__main__':
    app.run(host='192.168.0.157', port=5000, debug=True)
