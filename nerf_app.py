from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
from nerf_shooter import main as nerf_main

app = Flask(__name__)

# Initialize the Raspberry Pi camera
camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('nerf_index.html')

@app.route('/shoot_nerf', methods=['POST'])
def shoot_nerf():
    # Run your Python script here
    script_thread = threading.Thread(target=shoot_dart)
    script_thread.start()
    return jsonify({"status": "Script is running..."})

def shoot_dart():
    print("shoot nerf")
    # nerf_main()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
