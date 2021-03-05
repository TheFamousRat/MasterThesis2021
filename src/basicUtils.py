import bpy
import math

def RGBtoHSV(R,G,B):
	# min, max, delta;
	min_rgb = min( R, G, B )
	max_rgb = max( R, G, B )
	V = max_rgb

	delta = max_rgb - min_rgb
	if not delta:
		H = 0
		S = 0
		V = R # RGB are all the same.
		return H,S,V

	elif max_rgb: # != 0
		S = delta / max_rgb
	else:
		R = G = B = 0 # s = 0, v is undefined
		S = 0
		H = 0 # -1
		return H,S,V

	if R == max_rgb:
		H = ( G - B ) / delta # between yellow & magenta
	elif G == max_rgb:
		H = 2 + ( B - R ) / delta # between cyan & yellow
	else:
		H = 4 + ( R - G ) / delta # between magenta & cyan

	H *= 60 # degrees
	if H < 0:
		H += 360

	H = H * (math.pi / 180.0)
	
	return H,S,V

def colHSVDist(col1, col2):
	"""
	Calculates the distance between two colors in the HSV space
	:param col1: First HSV color
	:type col1: list
	:param col2: Second HSV color
	:type col2: list
	"""
	return math.pow((math.cos(col1[0]) * col1[1]) - (math.cos(col2[0]) * col2[1]), 2.0) + math.pow((math.sin(col1[0]) * col1[1]) - (math.sin(col2[0]) * col2[1]), 2.0)