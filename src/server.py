from flask import Flask, request
import motor_control

app = Flask(__name__)

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    x = data['x']  # horizontal position (-1 to 1)
    y = data['y']  # vertical position (-1 to 1)
    force = data['force'] # force (0 to 1)

    # calculate the speed of the left and right motors
    left_speed = (y + x) * force
    right_speed = (y - x) * force

    # limit the speed to be between -1 and 1
    left_speed = max(min(left_speed, 1), -1)
    right_speed = max(min(right_speed, 1), -1)

    # control the left motor
    if left_speed > 0:
        motor_control.setSpeed_L(left_speed, "forward")
    elif left_speed < 0:
        motor_control.setSpeed_L(-left_speed, "backward")
    else:
        motor_control.stop_L()

    # control the right motor
    if right_speed > 0:
        motor_control.setSpeed_R(right_speed, "forward")
    elif right_speed < 0:
        motor_control.setSpeed_R(-right_speed, "backward")
    else:
        motor_control.stop_R()

    return 'Command received'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
