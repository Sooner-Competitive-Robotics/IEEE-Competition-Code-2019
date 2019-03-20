import smbus
import time
import startup
import RPi.GPIO as GPIO
from vision import vision
from gpiozero import Button
from picamera import PiCamera

# IEEE competition code

address1 = 10						# Address to the drive nano
address2 = 20						# Address to the arm nano

bus = smbus.SMBus(1)
camera = PiCamera()
camera.resolution = (600, 600)
camera.rotation = 180

myvision = vision()
myNano = NanoManager()

# List of info to send. Format is [forward, side, distance]
data = []

while True:
	print('begin')
	
	# Get JSON file location
	
	# Drive to one location
	
	# Align to the cube
	while True:
		camera.capture("Center.jpg")
		
		# Cube is to the right
		if myvision.getCenter("center.jpg") == 1:
			data = [0, 1, 1]
			driveRobot(address1, data)
		# Cube is to the left
		elif myvision.getCenter("center.jpg") == -1:
			data = [0, -1, 1]
			driveRobot(address1, data)
		# Cube is centered. Move forward to pick cube up.
		elif myvision.getCenter("center.jpg") == 0:
			data = [1, 0, 6]
			driveRobot(address1, data)
			# Move arm and pick it up
			
		# Cube is not found; move on to another JSON location
		else:
			break
	
# Sends I2C signal then wait until the end
def driveRobot(address, data):
	bus.write_i2c_block_data(address, 0, data)
	time.sleep(myNano.getWaitTime(myNano.convertInchesToSteps(data[2])))
	
	
	
	
	
	
	