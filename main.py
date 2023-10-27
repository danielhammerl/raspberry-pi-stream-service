import cv2
from flask import Flask, Response
from datetime import datetime
import time
import os

dev_mode = True
try:
    stream_url = os.environ["STREAM_URL"]
except KeyError:
    dev_mode = False

if dev_mode == False:
    from subprocess import Popen

    p = Popen(["sh", "./stream-rtsp.sh"])

    time.sleep(10)

app = Flask(__name__)

def get_current_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%d.%m.%Y %H:%M:%S")
    return timestamp

rtsp_url = stream_url if dev_mode else 'tcp://localhost:8081'
print("rtsp url is: ", rtsp_url)
cap = cv2.VideoCapture(rtsp_url)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        timestamp = get_current_timestamp()

        # Overlay the timestamp on the frame
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
    response = Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return response

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
    print("Server started")
    try:
        p.terminate()
    except NameError:
        pass
