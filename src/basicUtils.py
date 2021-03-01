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

	return H,S,V

def getImagePixelColor_RGB(imPixels, width, x, y):
	"""
	:param im: List of pixels of the image texture from which to find the pixel
	:type im: list
	:param width: Width of the image
	:type width: int
	:param x: Pixel X-coordinate
	:type x: int
	:param y: Pixel Y-coordinate
	:type y: int
	:returns: 4-sized list representing RGBA pixel structure ([R, G, B, A])
	:rtype: list
	"""
	pixelIdx = ( y * width + x ) * 4

	return [
	imPixels[pixelIdx], # RED
	imPixels[pixelIdx + 1], # GREEN
	imPixels[pixelIdx + 2], # BLUE
	imPixels[pixelIdx + 3] # ALPHA
	]
    
def getImagePixelColor_HSV(imPixels, width, x, y):
	"""
	:param im: List of pixels of the image texture from which to find the pixel
	:type im: list
	:param width: Width of the image
	:type width: int
	:param x: Pixel X-coordinate
	:type x: int
	:param y: Pixel Y-coordinate
	:type y: int
	:returns: 3-sized list representing RGBA pixel structure ([H, S, V])
	:rtype: list
	"""
	pixelIdx = ( y * width + x ) * 4

	H, S, V = RGBtoHSV(imPixels[pixelIdx], imPixels[pixelIdx + 1], imPixels[pixelIdx + 2])
	return [H,S,V]

def getImagePixelColor_HS(imPixels, width, x, y):
	"""
	:param im: List of pixels of the image texture from which to find the pixel
	:type im: list
	:param width: Width of the image
	:type width: int
	:param x: Pixel X-coordinate
	:type x: int
	:param y: Pixel Y-coordinate
	:type y: int
	:returns: 2-sized list representing RGBA pixel structure ([H, S])
	:rtype: list
	"""
	pixelIdx = ( y * width + x ) * 4

	H, S, V = RGBtoHSV(imPixels[pixelIdx], imPixels[pixelIdx + 1], imPixels[pixelIdx + 2])
	return [H,S]