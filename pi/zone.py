#import neopixel
class Zone:
    pixels = None
    style = None
    color1 = None
    color2 = None
    color3 = None
    numcolors = None
    r = 255
    g = 0
    b = 0
    pasttime = 0
    pos = 0
    
    def reset( self, style, color1, color2, color3, numcolors ):
        self.style = style
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.numcolors = numcolors
        self.r = 255
        self.g = 0
        self.b = 0
        self.pasttime = 0
        self.pos = 0

    def circular_breathing( time ):
        return ( 1.0 - abs(2 * ( time / 3 ) - 1.0 ) ** 2 ) ** 0.5
    
    def hex_to_rgb( hex ):
        if hex:
            hex = hex.lstrip('#')
            return tuple( int( hex[i:i+2], 16 ) for i in ( 0, 2, 4 ) )
        return None

    def __init__( self, pixels, style, color1, color2, color3, numcolors ):
        self.pixels = pixels
        self.style = style
        self.color1 = self.hex_to_rgb(color1)
        self.color2 = self.hex_to_rgb(color2)
        self.color3 = self.hex_to_rgb(color3)
        self.numcolors = numcolors
    
    def process_colors( self, time ):
        if self.style:
            self.tick += 1
            if self.style == "SOLID":
                self.solid()
            elif self.style == "PULSE":
                self.pulse( time )
            elif self.style == "LINE":
                self.line()
            elif self.style == "RANIBOW":
                self.rainbow()
        else:
            for pixel in self.pixels:
                pixel = (0,0,0)
                pixel.brightness = 0

    def solid( self ):
        if self.numcolors == 1:
            for pixel in self.pixels:
                pixel = self.color1
                pixel.brightness = 1
        elif self.numcolors == 2:
            for i in range( len( self.pixels ) ):
                pixel = self.pixels[i]
                if i % 2:
                    pixel = self.color1
                else:
                    pixel = self.color2
                pixel.brightness = 1
        elif self.numcolors == 3:
            for i in range( len( self.pixels ) ):
                pixel = self.pixels[i]
                if i % 3 == 2:
                    pixel = self.color1
                elif i % 3 == 1:
                    pixel = self.color2
                else:
                    pixel = self.color3
                pixel.brightness = 1
    
    def pulse( self, time ):
        self.solid()
        for pixel in self.pixels:
            pixel.brightness = self.circular_breathing(time)
    
    def line( self, t ):
        diff = t - self.pasttime
        if diff >= 0.2:
            self.pos += 1
            if self.pos == 4:
                self.pos = 1
            self.pasttime = t
        if self.pos == 1:
            c1 = self.color1
            c2 = self.color2
            c3 = self.color3
        elif self.pos == 2:
            c1 = self.color3
            c2 = self.color1
            c3 = self.color2
        elif self.pos == 3:
            c1 = self.color2
            c2 = self.color3
            c3 = self.color1
        for i in range( len( self.pixels ) ):
            pixel = self.pixels[i]
            if i % 3 == 2:
                pixel = c1
            elif i % 3 == 1:
                pixel = c2
            else:
                pixel = c3
            pixel.brightness = 1

    def rainbow( self ):
        if self.r > 0 and self.b == 0:
            self.r -= 1
            self.g += 1
        if self.g > 0 and self.r == 0:
            self.g -= 1
            self.b += 1
        if self.b > 0 and self.g == 0:
            self.r += 1
            self.b -= 1
        for pixel in self.pixels:
            pixel = ( self.r, self.g, self.b )
            pixel.brightness = 1