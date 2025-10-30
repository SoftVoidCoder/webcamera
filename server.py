from flask import Flask, request, send_file, render_template_string
import os

app = Flask(__name__)
latest_screen = None

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Screen Monitor</title>
    <meta http-equiv="refresh" content="2">
</head>
<body>
    <h1>Live Screen Feed</h1>
    <img src="/latest_screen" width="1024" height="768">
</body>
</html>
'''

@app.route('/')
def control_panel():
    return render_template_string(HTML)

@app.route('/upload_screen', methods=['POST'])
def handle_screen():
    global latest_screen
    try:
        if 'file' in request.files:
            file = request.files['file']
            file.save('latest_screen.jpg')
            latest_screen = 'latest_screen.jpg'
    except Exception as e:
        print(f"Error: {e}")
    return 'OK'

@app.route('/latest_screen')
def get_latest_screen():
    if latest_screen and os.path.exists(latest_screen):
        return send_file(latest_screen, mimetype='image/jpeg')
    return 'No image'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)