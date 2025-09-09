from flask import Flask, request, jsonify, send_from_directory
from rpi_ws281x import Adafruit_NeoPixel, Color

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

# Function to set all LEDs to the same color
def set_color(r, g, b):
    """Set the same color on all LEDs."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()

# Function to set individual pixel colors from short data format
def set_pixels(pixel_data):
    """Set colors for each pixel based on short format: r1,g1,b1,r2,g2,b2,..."""
    values = list(map(int, pixel_data.split(',')))
    
    if len(values) % 3 != 0:
        return False  # Invalid data length
    
    num_pixels = len(values) // 3
    for i in range(num_pixels):
        r, g, b = values[i*3:(i+1)*3]
        if i < strip.numPixels():  # Ensure we do not exceed LED count
            strip.setPixelColor(i, Color(r, g, b))

    strip.show()
    return True

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
    if set_pixels(pixel_data):
        return jsonify({'status': 'OK'})
    else:
        return jsonify({'status': 'ERROR', 'message': 'Invalid data format'}), 400

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
    set_color(0, 0, 0)
    return jsonify({'status': 'OFF'})

# Run the server
if __name__ == '__main__':
    app.run(host='192.168.0.157', port=5000, debug=True)
from flask import Flask, request, jsonify, send_from_directory
from rpi_ws281x import Adafruit_NeoPixel, Color

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

# Function to set all LEDs to the same color
def set_color(r, g, b):
    """Set the same color on all LEDs."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()

# Function to set individual pixel colors from short data format
def set_pixels(pixel_data):
    """Set colors for each pixel based on short format: r1,g1,b1,r2,g2,b2,..."""
    values = list(map(int, pixel_data.split(',')))
    
    if len(values) % 3 != 0:
        return False  # Invalid data length
    
    num_pixels = len(values) // 3
    for i in range(num_pixels):
        r, g, b = values[i*3:(i+1)*3]
        if i < strip.numPixels():  # Ensure we do not exceed LED count
            strip.setPixelColor(i, Color(r, g, b))

    strip.show()
    return True

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

    if not pixel_data:  # Sprawdza, czy dane są puste
        return jsonify({'status': 'ERROR', 'message': 'No data provided'}), 400

    if set_pixels(pixel_data):
        return jsonify({'status': 'OK'})
    else:
        return jsonify({'status': 'ERROR', 'message': 'Invalid data format'}), 400


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
    set_color(0, 0, 0)
    return jsonify({'status': 'OFF'})

# Run the server
if __name__ == '__main__':
    app.run(host='192.168.0.157', port=5000, debug=True)
