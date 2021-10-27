#import neopixel
class Zone:
    pixels = None
    style = None
    color1 = None
    color2 = None
    color3 = None
    storage_color1 = None
    storage_color2 = None
    storage_color3 = None
    numcolors = None
    rainbow_r = 255
    rainbow_g = 0
    rainbow_b = 0
    pasttime = 0
    pos = 0
    
    def reset( self, style, color1, color2, color3, numcolors ):
        # Can this replace all of below?
        #self = Zone( self.pixels, style, color1, color2, color3, numcolors )
        self.style = style
        self.color1 = self.hex_to_rgb(color1)
        self.color2 = self.hex_to_rgb(color2)
        self.color3 = self.hex_to_rgb(color3)
        self.storage_color1 = self.color1
        self.storage_color2 = self.color2
        self.storage_color3 = self.color3
        self.numcolors = numcolors
        self.rainbow_r = 255
        self.rainbow_g = 0
        self.rainbow_b = 0
        self.pasttime = 0
        self.pos = 0

    def circular_breathing( self, time ):
        return ( 1.0 - abs(2 * ( time / 3 ) - 1.0 ) ** 2 ) ** 0.5
    
    def hex_to_rgb( self, hex ):
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
        self.storage_color1 = self.color1
        self.storage_color2 = self.color2
        self.storage_color3 = self.color3
        self.numcolors = numcolors
    
    def process_colors( self, time ):
        if self.style:
            if self.style == "SOLID":
                self.solid()
            elif self.style == "PULSE":
                self.pulse( time )
            elif self.style == "LINE":
                self.line()
            elif self.style == "RANIBOW":
                self.rainbow()
        else:
            self.pixels.fill( (0,0,0) )
            self.pixels.show()

    def solid( self ):
        if self.numcolors == 1:
            for i in range(len(self.pixels)):
                self.pixels[i] = self.color1
        elif self.numcolors == 2:
            for i in range( len( self.pixels ) ):
                if i % 2:
                    self.pixels[i] = self.color1
                else:
                    self.pixels[i] = self.color2
        elif self.numcolors == 3:
            for i in range( len( self.pixels ) ):
                if i % 3 == 2:
                    self.pixels[i] = self.color1
                elif i % 3 == 1:
                    self.pixels[i] = self.color2
                else:
                    self.pixels[i] = self.color3
        self.pixels.show()
    
    def pulse( self, time ):
        brightness = self.circular_breathing(time)
        self.color1 = self.storage_color1 * brightness
        self.color2 = self.storage_color2 * brightness
        self.color3 = self.storage_color3 * brightness
        self.solid()
    
    def line( self, t ):
        diff = t - self.pasttime
        if diff >= 0.2:
            self.pos += 1
            if self.numcolors <= 2:
                if self.pos == 3:
                    self.pos = 1
            else:
                if self.pos == 4:
                    self.pos = 1
            self.pasttime = t
        if self.numcolors == 3:
            if self.pos == 1:
                self.color1 = self.storage_color1
                self.color2 = self.storage_color2
                self.color3 = self.storage_color3
            elif self.pos == 2:
                self.color1 = self.storage_color3
                self.color2 = self.storage_color1
                self.color3 = self.storage_color2
            elif self.pos == 3:
                self.color1 = self.storage_color2
                self.color2 = self.storage_color3
                self.color3 = self.storage_color1
        elif self.numcolors == 2:
            if self.pos % 2:
                self.color1 = self.storage_color1
                self.color2 = self.storage_color2
            else:
                self.color1 = self.storage_color2
                self.color2 = self.storage_color1
        else:
            if self.pos % 2:
                self.color1 = self.storage_color1
                self.color2 = ( 0, 0, 0 )
            else:
                self.color1 = ( 0, 0, 0 )
                self.color2 = self.storage_color1
        self.pixels.show()

    def rainbow( self ):
        if self.rainbow_r > 0 and self.rainbow_b == 0:
            self.rainbow_r -= 1
            self.rainbow_g += 1
        if self.rainbow_g > 0 and self.rainbow_r == 0:
            self.rainbow_g -= 1
            self.rainbow_b += 1
        if self.rainbow_b > 0 and self.rainbow_g == 0:
            self.rainbow_r += 1
            self.rainbow_b -= 1
        for i in range(len(self.pixels)):
            self.pixels[i] = ( self.rainbow_r, self.rainbow_g, self.rainbow_b )
        self.pixels.show()