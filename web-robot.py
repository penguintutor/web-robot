#!/usr/bin/env python3
# RPi Magician Robot - 
# see http://www.penguintutor.com/rubyrobot
# web-robot.py
# Copyright Stewart Watkiss 2014


# This code is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

try:
    import RPi.GPIO as GPIO

except RuntimeError:
    print("Error importing RPi.GPIO! This must be run as root using sudo")

import sys, tty, termios
import picamera
import bottle
from bottle import route, request, response, template, static_file

app = bottle.Bottle()

# Camera settings
CAMERA_X = 1296
CAMERA_Y = 972
# Is camera upright / upside down
# Upside down = 180
CAMERA_ROTATE = 180


# Motor PINs
MOTOR1A = 17    #left fwd
MOTOR1B = 18    #left rev
MOTOR2A = 23    #right fwd
MOTOR2B = 22    #right rev

# freq of pwm outputs
PWM_FREQ = 50 #50hz

# uses processor pin numbering
GPIO.setmode(GPIO.BCM)

# speed = pwm duty cycle, 0 = off, 100 = max
speed = 75
# To change speed add or remove 10 - check for <0 and >100


# server ip address - set to 127.0.0.1 for local connections only, or change to actual address if require access direct from other computers (eg. smartphone) '' = all interfaces
HOST = ''
# unique port number - this happens to be the ip address used in the example setup without the dots
#PORT = 10551
# Using standard port as no other webserver running
PORT = 80
# length of a message - all network messages must be padded to this length 
#MSG_LEN = 20

DOCUMENT_ROOT = '/home/pi/robot'

# global for direction of motors (m1, m2)
current_direction = (0, 0)


# public files
# *** WARNING ANYTHING STORED IN THE PUBLIC FOLDER WILL BE AVAILABLE TO DOWNLOAD ***
@app.route ('/public/<filename>')
def server_public (filename):
    return static_file (filename, root=DOCUMENT_ROOT+"/public")



@app.route ('/control')
def control_robot():
    global current_direction
    global speed

    getvar_dict = request.query.decode()
    cmd = request.query.cmd
    if (cmd == 'motor') :
        
        # two motor values m1 and m2
        # If missing from url or not int then set to 0 = stop
        m1 = int(request.query.m1) or 0
        m2 = int(request.query.m2) or 0
        
        # check that m1 & m2 are valid - if either are invalid then set both to 0
        if (m1 >= 0 and m1 <= 2 and m2 >= 0 and m2 <= 2) :
            current_direction = (m1,m2)
        else :
            current_direction = (0,0)
        
        motor_change()

        return 'Motor changed to (' + str(current_direction[0]) + ' , ' + str(current_direction[1]) + ')'
    # speed set= sets an actual speed (0 to 100), chg = is a relative change
    elif (cmd == 'speed') :
        
        # is this a set request
        if 'set' in getvar_dict.keys():
            newSpeed = int(request.query.set) or -1
            if (newSpeed >= 0 and newSpeed <= 100) :
                speed = newSpeed
        elif 'chg' in getvar_dict.keys() :
            # zero means not change signal recieved - or set to 0 in either case no change to speed
            chgSpeed = int (request.query.chg) or 0
            newSpeed = speed + chgSpeed
            if (newSpeed < 0) :
                speed = 0
            elif (newSpeed > 100) :
                speed = 100
            else :
                speed = newSpeed
        else :
            return "No change"
            

        return 'Speed changed to '+str(speed);
    return "Command not recognised"
    


@app.route ('/')
def server_home ():
    return static_file ('index.html', root=DOCUMENT_ROOT)




@app.route ('/status')
def webcontrol():
	return "OK"



@app.route ('/photocapture')
def take_photo():
    with picamera.PiCamera() as camera:
        camera.resolution = (CAMERA_X, CAMERA_Y)
        camera.rotation = CAMERA_ROTATE
        camera.exif_tags['IFD0.Artist'] = 'Penguintutor Robot'
        camera.capture('/home/pi/robot/photos/photo.jpg')
        camera.close()
    return "OK"


@app.route ('/photo')
def view_photo():
    return static_file("photo.jpg", root='/home/pi/robot/photos/')




# Change the motor outputs based on the current_direction and speed global variables
def motor_change():
    #print "Update motors to " + str(current_direction[0]) + " " + str(current_direction[1])
    # motor 1
    if (current_direction[0] == 1) :
        pin1A.ChangeDutyCycle(speed)
        pin1B.ChangeDutyCycle(0)
    elif (current_direction[0] == 2) :
        pin1A.ChangeDutyCycle(0)
        pin1B.ChangeDutyCycle(speed)
    # if 0 (stop) or invalid stop anyway
    else :
        pin1A.ChangeDutyCycle(0)
        pin1B.ChangeDutyCycle(0)
    # motor 2
    if (current_direction[1] == 1) :
        pin2A.ChangeDutyCycle(speed)
        pin2B.ChangeDutyCycle(0)
    elif (current_direction[1] == 2) :
        pin2A.ChangeDutyCycle(0)
        pin2B.ChangeDutyCycle(speed)
    # if 0 (stop) or invalid stop anyway
    else :
        pin2A.ChangeDutyCycle(0)
        pin2B.ChangeDutyCycle(0)
 



# direction based on number keypad 
# 8 = fwd, 2 = rev, 4 = left, 5 = right, 7 = fwd left, 9 = fwd right, 1 = rev left, 3 = rev right
### These are from the command line version - they are not used in this version. This list will be removed in future edits
direction = {
    # number keys
    '1' : (2, 0),
    '2' : (2, 2),
    '3' : (0, 2),
    '4' : (1, 2),
    '5' : (0, 0),
    '6' : (2, 1),
    '7' : (1, 0),
    '8' : (1, 1),
    '9' : (0, 1)
}




# setup pins
GPIO.setup(MOTOR1A, GPIO.OUT)
GPIO.setup(MOTOR1B, GPIO.OUT)
GPIO.setup(MOTOR2A, GPIO.OUT)
GPIO.setup(MOTOR2B, GPIO.OUT)
#GPIO.setup(PWM_ALL, GPIO.OUT)

pin1A = GPIO.PWM(MOTOR1A, PWM_FREQ)
pin1B = GPIO.PWM(MOTOR1B, PWM_FREQ)
pin2A = GPIO.PWM(MOTOR2A, PWM_FREQ)
pin2B = GPIO.PWM(MOTOR2B, PWM_FREQ)

pin1A.start (0)
pin1B.start (0)
pin2A.start (0)
pin2B.start (0)



app.run(host=HOST, port=PORT)

    
# Stop PWM and cleanup - only called if exit from bottle server        
pin1A.stop()
pin1B.stop()
pin2A.stop()
pin1B.stop()
GPIO.cleanup()




