from flask import Flask, request, jsonify, send_from_directory
from rpi_ws281x import Adafruit_NeoPixel, Color
import threading
import time

app = Flask(__name__, static_folder='static')

# LED configuration
LED_COUNT = 237
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 25  # Default brightness
LED_INVERT = False
LED_CHANNEL = 0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
running_animation = None  # Przechowuje aktualnie uruchomiona animacje

# Function to set all LEDs to the same color
def set_color(r, g, b):
    """Ustawienie jednego koloru dla calego paska i zatrzymanie animacji."""
    global running_animation
    running_animation = None  # Zatrzymanie aktualnej animacji

    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()

# Function to set individual pixel colors from short data format
def set_pixels(pixel_data):
    """Set colors for selected pixels in format: r1,g1,b1,r2,g2,b2,..."""
    values = list(map(int, pixel_data.split(',')))

    if len(values) % 3 != 0:
        return False  # Invalid data length

    num_pixels = len(values) // 3
    for i in range(num_pixels):
        r, g, b = values[i*3:(i+1)*3]
        if i < strip.numPixels():  # Ensure within LED range
            strip.setPixelColor(i, Color(r, g, b))

    strip.show()
    return True

# Function to generate rainbow colors
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

# Function to display a rainbow animation
def rainbow(strip, wait_ms):
    """Nieskonczona animacja teczy, zatrzymywana przez set_color lub off."""
    global running_animation
    running_animation = "rainbow"

    while running_animation == "rainbow":
        for j in range(256):
            if running_animation != "rainbow":
                return  # Przerwij petle, jesli animacja zostala zatrzymana

            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)  # Opoznienie ustawiane przez uzytkownika

# Route for serving the HTML page
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Route to set a single color for all LEDs
@app.route('/set_color', methods=['GET'])
def change_color():
    r = int(request.args.get('r', 0))
    g = int(request.args.get('g', 0))
    b = int(request.args.get('b', 0))
    set_color(r, g, b)
    return jsonify({'status': 'OK', 'color': (r, g, b)})

# Route to set individual pixels using compact format
@app.route('/set_pixels', methods=['GET'])
def set_pixels_api():
    pixel_data = request.args.get('data', '')

    if not pixel_data:  # Check if data is empty
        return jsonify({'status': 'ERROR', 'message': 'No data provided'}), 400

    if set_pixels(pixel_data):
        return jsonify({'status': 'OK'})
    else:
        return jsonify({'status': 'ERROR', 'message': 'Invalid data format'}), 400

# Route to start animations with adjustable delay
@app.route('/start_animation', methods=['GET'])
def start_animation():
    global running_animation
    animation = request.args.get('effect', 'rainbow')
    delay = int(request.args.get('delay', 20))  # Pobranie opóźnienia

    # Zatrzymaj poprzednia animacje przed uruchomieniem nowej
    running_animation = None  
    time.sleep(0.1)  # Krótkie opóźnienie, aby zatrzymać starą animację

    if animation == "rainbow":
        running_animation = animation  # Oznacz nową animację jako uruchomioną
        threading.Thread(target=rainbow, args=(strip, delay)).start()
        return jsonify({'status': 'OK', 'animation': 'rainbow', 'delay': delay})

    return jsonify({'status': 'ERROR', 'message': 'Unknown animation'}), 400

    
    
# Route to adjust LED brightness
@app.route('/set_brightness', methods=['GET'])
def set_brightness():
    global strip
    brightness = int(request.args.get('brightness', 25))
    brightness = max(0, min(255, brightness))  # Limit between 0 and 255

    strip.setBrightness(brightness)
    strip.show()
    return jsonify({'status': 'OK', 'brightness': brightness})

# Route to turn off LEDs
@app.route('/off', methods=['GET'])
def turn_off():
    global running_animation
    running_animation = None  # Zatrzymanie aktualnej animacji
    set_color(0, 0, 0)
    return jsonify({'status': 'OFF'})

# Run the server
if __name__ == '__main__':
    app.run(host='192.168.0.157', port=5000, debug=True)
