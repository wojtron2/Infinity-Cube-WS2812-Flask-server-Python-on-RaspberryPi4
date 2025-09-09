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
LED_BRIGHTNESS = 25
LED_INVERT = False
LED_CHANNEL = 0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

running_animation = None  # Stores currently running animation

# Set all LEDs to the same color and stop animations
def set_color(r, g, b):
    global running_animation
    running_animation = None
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()

# Set individual pixel colors from short data format
def set_pixels(pixel_data):
    """Set colors for selected pixels in format: r1,g1,b1,r2,g2,b2,..."""

    # Usuwanie nowych linii i spacji
    pixel_data = pixel_data.strip().replace("\n", "").replace("\r", "")

    print(f"Received raw data: {repr(pixel_data)}")  # Debug input

    if not pixel_data:
        print("Error: No data received!")
        return False

    try:
        values = list(map(int, pixel_data.split(',')))
    except ValueError:
        print(f"Error: Cannot convert values to integers! Data received: {repr(pixel_data)}")
        return False  # Data format error

    if len(values) % 3 != 0:
        print(f"Invalid number of values ({len(values)})! Must be a multiple of 3. Data received: {repr(pixel_data)}")
        return False

    num_pixels = min(len(values) // 3, strip.numPixels())  # Limit to available LEDs

    for i in range(num_pixels):
        r, g, b = values[i*3:(i+1)*3]
        print(f"LED {i}: R={r}, G={g}, B={b}")  # Debug for each LED
        strip.setPixelColor(i, Color(r, g, b))

    strip.show()
    print("Pixels set successfully!")
    return True

# Generate rainbow colors
def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

# Infinite rainbow animation, stops when set_color or off is called
def rainbow(strip, wait_ms):
    global running_animation
    running_animation = "rainbow"

    while running_animation == "rainbow":
        for j in range(256):
            if running_animation != "rainbow":
                return
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/set_color', methods=['GET'])
def change_color():
    r = int(request.args.get('r', 0))
    g = int(request.args.get('g', 0))
    b = int(request.args.get('b', 0))
    set_color(r, g, b)
    return jsonify({'status': 'OK', 'color': (r, g, b)})

@app.route('/set_pixels', methods=['GET'])
def set_pixels_api():
    pixel_data = request.args.get('data', '')

    if not pixel_data:
        return jsonify({'status': 'ERROR', 'message': 'No data provided'}), 400

    if set_pixels(pixel_data):
        return jsonify({'status': 'OK'})
    else:
        return jsonify({'status': 'ERROR', 'message': 'Invalid data format'}), 400

@app.route('/start_animation', methods=['GET'])
def start_animation():
    global running_animation
    animation = request.args.get('effect', 'rainbow')
    delay = int(request.args.get('delay', 20))

    running_animation = None
    time.sleep(0.1)

    if animation == "rainbow":
        running_animation = animation
        threading.Thread(target=rainbow, args=(strip, delay)).start()
        return jsonify({'status': 'OK', 'animation': 'rainbow', 'delay': delay})

    return jsonify({'status': 'ERROR', 'message': 'Unknown animation'}), 400

@app.route('/set_brightness', methods=['GET'])
def set_brightness():
    brightness = int(request.args.get('brightness', 25))
    brightness = max(0, min(255, brightness))
    strip.setBrightness(brightness)
    strip.show()
    return jsonify({'status': 'OK', 'brightness': brightness})

@app.route('/off', methods=['GET'])
def turn_off():
    global running_animation
    running_animation = None
    set_color(0, 0, 0)
    return jsonify({'status': 'OFF'})

if __name__ == '__main__':
    app.run(host='192.168.0.157', port=5000, debug=True)
