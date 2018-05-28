
import sys

def cal(x,y,z):
	return x / (x+y+z), y / (x+y+z), z / (x+y+z), 

if __name__ == "__main__":
	print(cal(255,100,10))

	