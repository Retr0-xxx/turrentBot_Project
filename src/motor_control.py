from gpiozero import Motor, PWMOutputDevice
from time import sleep

# define pins on the Raspberry Pi that are connected to LN298N
# Input pins of LN298N, controls the direction of motor rotation
in1 = 23 
in2 = 24  
in3 = 25  
in4 = 8 
# Enable pins of LN298N, controls the speed of the motor
ena = 18  
enb = 12  

leftMotor = Motor(forward=in1, backward=in2, enable=ena)
rightMotor = Motor(forward=in3, backward=in4, enable=enb)

# Set the speed of the left motor, the speed is between 0 and 1, direction is either "forward" or "backward"
def setSpeed_L(speed, direction):
    if direction == "forward":
        leftMotor.forward(speed)
        print("left motor set forward speed: "+str(speed))
    elif direction == "backward":
        leftMotor.backward(speed)
        print("left motor set backward speed: "+str(speed))

# Set the speed of the right motor, the speed is between 0 and 1, direction is either "forward" or "backward"
def setSpeed_R(speed, direction):
    if direction == "forward":
        rightMotor.forward(speed)
        print("right motor set forward speed: "+str(speed))
    elif direction == "backward":
        rightMotor.backward(speed)
        print("right motor set backward speed: "+str(speed))

def stopAll():
    leftMotor.stop()
    rightMotor.stop()
    print("stopped all motors")

def stop_L():
    leftMotor.stop()
    print("stopped left motor")

def stop_R():
    rightMotor.stop()
    print("stopped right motor")

