import smbus
import time
import startup
import math
import RPi.GPIO as GPIO
from vision import vision
from gpiozero import Button
from picamera import PiCamera
import jsonread

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
data = []cd

while True:
	print('begin')
	
	# Get JSON file location
	data = jsonread()
	size = data["size"]
	# no way block is at 4,4 (starting location of robot)
	# no way closest block is 5 feet away
	minDist = 5 # feet
	minX = 4
	minY = 4

	# interates through all coordinates and finds minimum distance and at what coordinates
	while (size > 0):
		print(size)
		print("\n")
		dist = abs(math.sqrt(math.pow((data["x coords"][size - 1] - 4), 2)+math.pow((data["y coords"][size - 1] - 4), 2)))
		if (dist < minDist):
			minX = data["x coords"][size - 1]
			minY = data["y coords"][size - 1]
			minDist = dist
		size = size - 1
	
	print("MinX:", minX)
	print("\n")
	print("MinY:", minY)
	print("\n")
	
	# Drive to one location
		# if y coordinate is < 4 turn 180, > 4 nothing, = 4 turn 90 or -90 depending on x coor
		# if x coordinate is < 4 strafe left, > 4 strafe right, else nothing
		# stop one block away from actual location maybe?
		
	if (minY == 4):
		if (minX < 4):
			# turn in place -90
		else:
			# turn in place 90
	else if (minY > 4):
		if (minX < 4):
			# strafe left
		else if (minX > 4):
			# strafe right
	
	else if (minY < 4):
		#turn 180
		if (minX < 4):
			#strafe right (reverse because we turned 180)
		else if (minX > 4):
			#strafe left
			
	#drive up to cube 
	# if y != 4, drive (abs(y coord - 4ft) - 1 ft)
	# if y == 4, drive (abs(x coord - 4ft) - 1 ft)
	
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


def moveArm(address, data):
	bus.write_i2c_block_data(address2, 0, data)
	time.sleep(2) # figure out how long to wait for moving arm and claw
	