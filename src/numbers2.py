# Import all board pins.
import time
import board
import busio
from adafruit_ht16k33 import matrix
from array import *

num_zero = [
[0,1,1,0],
[1,0,0,1],
[1,0,0,1],
[1,0,0,1],
[1,0,0,1],
[1,0,0,1],
[1,0,0,1],
[0,1,1,0]
]

num_one = [
	[0,0,1,0],
	[0,1,1,0],
	[1,0,1,0],
	[0,0,1,0],
	[0,0,1,0],
	[0,0,1,0],
	[0,0,1,0],
	[1,1,1,1]
]

num_two = [
	[0,1,1,0],
	[1,0,0,1],
	[0,0,0,1],
	[0,0,0,1],
	[0,1,1,0],
	[1,0,0,0],
	[1,0,0,0],
	[1,1,1,1]
]

num_three = [
	[0,1,1,0],
	[1,0,0,1],
	[0,0,0,1],
	[1,1,1,0],
	[0,0,0,1],
	[0,0,0,1],
	[1,0,0,1],
	[0,1,1,0]
]

num_four = [
	[0,0,0,1],
	[1,0,0,1],
	[1,0,0,1],
	[1,0,0,1],
	[1,1,1,1],
	[0,0,0,1],
	[0,0,0,1],
	[0,0,0,1]
]
num_five = [
	[1,1,1,1],
	[1,0,0,0],
	[1,0,0,0],
	[1,1,1,0],
	[0,0,0,1],
	[0,0,0,1],
	[1,0,0,1],
	[0,1,1,0]
]
num_six = [
	[0,1,1,0],
	[1,0,0,1],
	[1,0,0,0],
	[1,1,1,0],
	[1,0,0,1],
	[1,0,0,1],
	[1,0,0,1],
	[0,1,1,0]
]

num_seven = [
	[1,1,1,1],
	[1,0,0,1],
	[0,0,0,1],
	[0,0,1,0],
	[0,1,0,0],
	[0,1,0,0],
	[0,1,0,0],
	[0,1,0,0]
]

num_eight = [
	[0,1,1,0],
	[1,0,0,1],
	[1,0,0,1],
	[0,1,1,0],
	[1,0,0,1],
	[1,0,0,1],
	[1,0,0,1],
	[0,1,1,0]
]

num_nine = [
	[0,1,1,0],
	[1,0,0,1],
	[1,0,0,1],
	[1,0,0,1],
	[0,1,1,1],
	[0,0,0,1],
	[1,0,0,1],
	[0,1,1,0]
]

number_set = [num_zero,num_one,num_two,num_three,num_four,num_five,num_six,num_seven,num_eight,num_nine]

# Face display.  Rotate so the connectors are on the right side. The origin is the south-east corner
# 0,0 - south-east
# Rotate 90deg clockwise
# 7,0 - south-west
# Rotate 90deg clockwise
# 0,7 - north-east
# Rotate 90deg clockwise
# 7,7 - north-west
origx = 7
origy = 7

def mymatrix_set(row, col):
	matrix[col, row] = 1

def mymatrix_pixel(x, y):
	if (origx == 0 and origy == 0):
		matrix[x,y] = 1
	if (origx == 7 and origy == 0):
		matrix[7-x,y] = 1
	if (origx == 7 and origy == 7):
		matrix[7-y,7-x] = 1
	if (origx == 0 and origy == 7):
		matrix[x,7-y] = 1

def show_number_from_array(x,y, num_array):
	ix = 0
	iy = 7
	for r in num_array:
		for c in r:
			if (c==1):
				mymatrix_pixel(ix % 4+x,iy+y)
			ix += 1
		iy -= 1

def show_number(x, y, n):
	matrix.fill(0)
	if (n > 99):
		show_number_from_array(x, y, number_set[0])
		show_number_from_array(x, y, number_set[0])
	if (n < 10):
		show_number_from_array(x, y, number_set[0])
		show_number_from_array(x+4, y, number_set[n])
	else:
		tens,ones=divmod(n,10)
		show_number_from_array(x, y, number_set[tens])
		show_number_from_array(x+4, y, number_set[ones])
			
def matrix_fill(c):
	matrix.fill(c)

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# creates a 8x8 matrix:
matrix = matrix.Matrix8x8(i2c)

# edges of an 8x8 matrix
x_max = 8
y_max = 8

#show_number(0,0, 1)

# Clear the matrix.
#for i in range(100):
#	matrix.fill(0)
#	show_number(0,0,i)
#	time.sleep(0.3)

#zero2(0,0)
#zero2(4,0)

#time.sleep(5)

#matrix.fill(0)


