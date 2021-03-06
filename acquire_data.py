#!/usr/bin/env python
########################################################################
# This example controls the GoPiGo and using a PS3 Dualshock 3 controller
#
# http://www.dexterindustries.com/GoPiGo/
# History
# ------------------------------------------------
# Author     	Date      		Comments
# Karan Nayan   11 July 14		Initial Authoring
'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''
#
# left,right,up,down to control
# cross to stop
# left joy to turn the camera servo
# l2 to increase speed
# r2 to decrease speed
########################################################################
from ps3 import *  # Import the PS3 library
from gopigo import *  # Import the GoPiGo library
import picamera

print "Initializing"
camera = picamera.PiCamera()
camera.vflip = True
camera.hflip = True
# camera.led = False
# camera.brightness = 60
camera.resolution = (320, 240)

# wait for the camera adjust the gain
print "Warming up camera"
time.sleep(2)

p = ps3()  # Create a PS3 object
print "Done"
s = 80  # Initializ
pulses = 4
imgid = 0
recording = False

enable_encoders()
enc_tgt(1,1,1)
fwd()

if not os.path.exists("images"):
	os.makedirs("images")
	os.makedirs("images/forward")
	os.makedirs("images/left")
	os.makedirs("images/right")


while True:
	p.update()  # Read the ps3 values
	# if read_enc_status() != 0:
	# 	time.sleep(0.01)
	# 	continue
	stoped = False
	set_speed(s)  # Update the speed
	if p.up:  # If UP is pressed move forward
		camera.capture('images/forward/image' + str(imgid) + '.jpg', use_video_port=True)
		# enc_tgt(1,1,pulses)
		fwd()
	elif p.left:  # If LEFT is pressed turn left
		camera.capture('images/left/image' + str(imgid) + '.jpg', use_video_port=True)
		# enc_tgt(0,1,pulses)
		left()
	elif p.right:  # If RIGHT is pressed move right
		camera.capture('images/right/image' + str(imgid) + '.jpg', use_video_port=True)
		# enc_tgt(1,0,pulses)
		right()
	elif p.down:  # If DOWN is pressed go back
		bwd()
	elif p.circle:
		led_on(LED_L)
		led_on(LED_R)
	elif p.square:
		camera.capture('image' + str(imgid) + '.jpg')
	elif p.triangle:
		if not recording:
			camera.start_recording('video.h264')
			recording = True
	elif p.cross:
		if recording:
			camera.stop_recording()
			recording = False
	else:
		stop()
		led_off(LED_L)
		led_off(LED_R)
		stoped = True

	if not stoped:
		imgid += 1

	if p.l2:  # Increase the speed if L2 is pressed
		print s
		s += 30
		if s > 255:
			s = 255
	if p.r2:  # Decrease the speed if R2 is pressed
		print s
		s -= 30
		if s < 0:
			s = 0
	x = (p.a_joystick_left_x + 1) * 75+6
	servo(int(x))  # Turn servo a/c to left joy movement
	# time.sleep(3)