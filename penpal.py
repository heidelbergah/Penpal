"""
This library contains all the functions needed to operate penpal.

drawTxtFile() should be the only function you need to call. To change where penpal moves, just
update the positions.txt file itself.

Penpal always starts with it's pen down, so make sure to account for this!

positions.txt should follow a similar format as below:

    positions.txt:

t      // Place pen down 
3,3    // Move to 3, 3
4,7    // Move to 4, 7
t      // Lift pen up
10,10  // so on...
t

"""

from gpiozero import Servo
import math
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

# Servo initializations. Min and max pulse widths correlate to the min and max degrees the servo can rotate to. These should not be changed.
rootServo = Servo(13, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
innerServo = Servo(19, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
penServo = Servo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
# Arm length should not change. Value is in millimeters
armLength = 10.5
# Duration the servos should sleep between each movement
sleepVal = 0.01
# For some reason, the servos want to be at 90 degrees at the start of each program.
currentX = 5
currentY = 5
# Is the pen down or up?
penDown = False

# x; X value of pen
# y; Y value of pen
# l; Length of arms in cm
# rootServo; Servo at base of plotter
# innerServo; Servo at middle of plotter
# This function calculates the needed angles of the servos for the pen
# to be placed at (x, y)
def move(x, y):
    h = math.sqrt((x ** 2) + (y ** 2))
    theta1 = math.degrees(math.asin((h/2)/armLength)) * 2
    innerAngle = abs(180 - theta1)
    theta2 = (180 - theta1) / 2
    theta3 = 0

    if x >= y:
        theta3 = math.degrees(math.asin(y/h))
    else:
        theta3 = 180 - (math.degrees(math.asin(x/h)) + 90)

    rootAngle = theta2 + theta3

    rootServo.value = standardize(rootAngle)
    innerServo.value = standardize(innerAngle)

    global currentX
    global currentY
    currentX = x
    currentY = y

    sleep(sleepVal)


# Simply moves the pen down if up, and moves the pen up if down
def togglePen():
    if(penServo.value == 0):
        penServo.value = 1
    else:
        penServo.value = 0
    sleep(sleepVal+0.3)


# angle; Angle ment to be standardized
# This function standardizes an angle to be used by the servo motors.
# Values must be standardized between -1 and 1.
# The library requires the angle to be between -1 and 1, so this just sets out angle to the correct ratio
def standardize(angle):
    return (angle / 90) - 1


# x; X position to move to
# y; Y position to move to
# Wicked fucking proud of this function.
# We start by finding the angle between the point we're currently located, and the point we want to move to.
# Once we have this angle, we can slowly move along this angle until we reach to a point that's close enough
# to our desired destination. 
def straightMove(x, y):
    increment = 0.05 # How much we move each iteration
    newX = currentX 
    newY = currentY
    angle = math.atan2((y - newY), (x - newX))
    while True:
        # The following just moves the x and y in a way that their hypotenuse equals our increment value
        newX += math.cos(angle) * increment
        newY += math.sin(angle) * increment
        if(closeEnough(newX, newY, x, y, increment)): # If we're close enough to our target plot, just move to it
            move(x, y)
            break
        move(newX, newY)


# nX; newX value
# nY; newY value
# tX; target x value
# tY; target y value
# i; increment valaue
# Check to see if we're "close enough" to our target plot
def closeEnough(nX, nY, tX, tY, i):
    if(abs((nX-tX)) <= i and abs(nY-tY) <= i):
        return True
    return False


# Opens up the positions.txt file and moves penpal to each plot.
# Also lifts the pen.
def drawTxtFile():
    file = open("positions.txt", "r")
    line = file.readline()
    global penDown

    while line:
        if line[0] == "t":
            togglePen()
            penDown = not penDown # Flip boolean value
        else:
            x = line.partition(",")[0]
            y = line.partition(",")[2]
            if penDown:
                straightMove(float(x), float(y))
            else:
                move(float(x), float(y)) # Because the pen is up, we don't need to move in a straight line
        line = file.readline()

    file.close()

    # Move pen back to up position
    if penDown:
        penDown = not penDown
        togglePen()


# Party time!
def dance():
    global sleepVal
    originalSleepVal = sleepVal
    sleepVal = 0.5
    move(5,5)
    move(1,15)
    move(3,7)
    move(5,15)
    move(7,7)
    move(9,15)
    move(5,5)
    sleepVal = originalSleepVal

