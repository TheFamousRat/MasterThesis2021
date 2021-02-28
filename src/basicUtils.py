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

def getImagePixel(im, x, y):
    """
    :param im: Image texture from which to find the pixel
    :type im: Image
    :param x: Pixel X-coordinate
    :type x: int
    :param y: Pixel Y-coordinate
    :type y: int
    :returns: 4-sized list representing RGBA pixel structure ([R, G, B, A])
    :rtype: list
    """
    pixelIdx = ( y * im.size[0] + x ) * 4

    return [
    im.pixels[pixelIdx], # RED
    im.pixels[pixelIdx + 1], # GREEN
    im.pixels[pixelIdx + 2], # BLUE
    im.pixels[pixelIdx + 3] # ALPHA
    ]