import socketio
import eventlet
from flask import Flask, Response
import motor_control
import cv2
import base64
import numpy as np
from picamera2 import Picamera2

app2 = Flask(__name__)

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, app2)



camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()

def generate_frames():
    while True:
        eventlet.sleep(2)
        frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app2.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@sio.event
def connect(sid,environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
def move(sid, data):
    x = data['x']
    y = data['y']
    force = data['force']

    left_speed = (y + x) * force
    right_speed = (y - x) * force

    left_speed = max(min(left_speed, 1), -1)
    right_speed = max(min(right_speed, 1), -1)

    if left_speed > 0:
        motor_control.setSpeed_L(left_speed, "forward")
    elif left_speed < 0:
        motor_control.setSpeed_L(-left_speed, "backward")
    else:
        motor_control.stop_L()

    if right_speed > 0:
        motor_control.setSpeed_R(right_speed, "forward")
    elif right_speed < 0:
        motor_control.setSpeed_R(-right_speed, "backward")
    else:
        motor_control.stop_R()

def generate_frames():
    while True:
        frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == '__main__':
    #listen to all incoming connections on port 8080
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), app)


