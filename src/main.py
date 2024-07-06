import motor_control
from time import sleep

#test motor function
try:
    while True:
        motor_control.setSpeed_L(0.5, "forward")
        motor_control.setSpeed_R(0.5, "forward")
        sleep(2)
        motor_control.setSpeed_L(0.5, "backward")
        motor_control.setSpeed_R(0.5, "backward")
        sleep(2)
        motor_control.setSpeed_L(0.5, "forward")
        motor_control.setSpeed_R(0.5, "backward")
        sleep(2)
        motor_control.setSpeed_L(0.5, "backward")
        motor_control.setSpeed_R(0.5, "forward")
        sleep(2)
except KeyboardInterrupt:
    motor_control.stopAll()
    print("stop")
