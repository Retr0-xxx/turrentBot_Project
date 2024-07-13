import socketio
import eventlet
from flask import Flask, Response
import motor_control
import cv2
import base64
import numpy as np
from picamera2 import Picamera2

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

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

def startServer():
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), app)


