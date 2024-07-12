import socketio
import eventlet
from flask import Flask
import motor_control
import cv2
import base64
import numpy as np

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# 摄像头初始化
camera = cv2.VideoCapture(0)  # 0代表默认摄像头，也可以用Raspberry Pi摄像头的地址

def encode_frame(img):
    """对帧进行编码为JPEG格式并转为Base64字符串"""
    _, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{jpg_as_text}"

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

def video_stream():
    """不断从摄像头读取帧，编码并发送"""
    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                break
            image_text = encode_frame(frame)
            sio.emit('video_frame', {'data': image_text}, skip_sid=True)
    finally:
        camera.release()
    
if __name__ == '__main__':

    eventlet.spawn(video_stream) # 启动视频流线程
    #listen to all incoming connections on port 8080
    eventlet.wsgi.server(eventlet.listen(('192.168.1.201', 8080)), app)

# pip install opencv-python-headless

