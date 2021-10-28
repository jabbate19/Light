#import neopixel
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.SparklePulse import SparklePulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.sequence import AnimationSequence
class Zone2:
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
    loop = 1
    start = None
    end = None

    _solid = None
    _blink = None
    _color_cycle = None
    _chase = None
    _comet = None
    _pulse = None
    _sparkle = None
    _sparkle_pulse = None
    _rainbow = None
    _rainbow_chase = None
    _rainbow_comet = None
    _rainbow_sparkle = None

    
    def reset( self, style, color1, color2, color3, numcolors ):
        self.__init__( self.pixels, style, color1, color2, color3, numcolors, self.start, self.end )

    def breathing( self ):
        self.pos += 1
        if self.pos >= 200:
            self.pos = 0
        return ( 1.0 - ( abs(2 * ( self.pos / 200 ) - 1.0 ) ) )
    
    def hex_to_rgb( self, hex ):
        if hex:
            hex = hex.lstrip('#')
            return tuple( int( hex[i:i+2], 16 ) for i in ( 0, 2, 4 ) )
        return None

    def __init__( self, pixels, style, color1, color2, color3, numcolors, start = None, end = None ):
        self.pixels = pixels
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
        if start == None:
            self.start = 0
            self.end = pixels.n
        else:
            self.start = start
            self.end = end
        self.pos = self.start
        self.loop = 1
        self._solid = Solid(pixels, color = self.color1 )
        self._blink = [
            Blink(pixels, speed=0.5, color = self.color1 ),
            AnimationSequence(
                Blink(pixels, speed=0.5, color = self.color1 ),
                Blink(pixels, speed=0.5, color = self.color2 ),
                advance_interval=1
            ),
            AnimationSequence(
                Blink(pixels, speed=0.5, color = self.color1 ),
                Blink(pixels, speed=0.5, color = self.color2 ),
                Blink(pixels, speed=0.5, color = self.color3 ),
                advance_interval=1
            )
        ]
        self._color_cycle = ColorCycle(pixels, 0.5, colors=[self.color1, self.color2, self.color3])
        self._chase = [
            Chase(pixels, speed=0.1, color = self.color1, size = 3 ),
            AnimationSequence(
                Chase(pixels, speed=0.1, color = self.color1, size = 3 ),
                Chase(pixels, speed=0.1, color = self.color2, size = 3 ),
                advance_interval=0.1*60
            ),
            AnimationSequence(
                Chase(pixels, speed=0.1, color = self.color1, size = 3 ),
                Chase(pixels, speed=0.1, color = self.color2, size = 3 ),
                Chase(pixels, speed=0.1, color = self.color3, size = 3 ),
                advance_interval=0.1*60
            )
        ]
        self._comet = [
            Comet(pixels, speed=0.01, color = self.color1, size = 3, bounce = True ),
            AnimationSequence(
                Comet(pixels, speed=0.01, color = self.color1, size = 3, bounce = True ),
                Comet(pixels, speed=0.01, color = self.color2, size = 3, bounce = True ),
                advance_interval=0.01*60*2
            ),
            AnimationSequence(
                Comet(pixels, speed=0.01, color = self.color1, size = 3, bounce = True ),
                Comet(pixels, speed=0.01, color = self.color2, size = 3, bounce = True ),
                Comet(pixels, speed=0.01, color = self.color3, size = 3, bounce = True ),
                advance_interval=0.01*60*2
            )
        ]
        self._pulse = [
            Pulse(pixels, speed=0.1, color = self.color1 ),
            AnimationSequence(
                Pulse(pixels, speed=0.1, color = self.color1 ),
                Pulse(pixels, speed=0.1, color = self.color2 ),
                advance_interval=0.1*60
            ),
            AnimationSequence(
                Pulse(pixels, speed=0.1, color = self.color1 ),
                Pulse(pixels, speed=0.1, color = self.color2 ),
                Pulse(pixels, speed=0.1, color = self.color3 ),
                advance_interval=0.1*60
            )
        ]
        self._sparkle = Sparkle(pixels, speed=0.05, color = self.color1 )
        self._sparkle_pulse = Sparkle(pixels, speed=0.05, color = self.color1 )
        self._rainbow = Rainbow( pixels, speed = 0.1 )
        self._rainbow_chase = RainbowChase( pixels, speed=0.1, size=5, spacing=3)
        self._rainbow_comet = RainbowComet( pixels, speed=0.1, tail_length=7, bounce=True)
        self._rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)
        
    
    def process_colors( self ):
        animation = None
        if self.style == "SOLID":
            animation = self._solid
        elif self.style == "BLINK":
            animation = self._blink[ self.numcolors - 1 ]
        elif self.style == "COLOR CYCLE":
            animation = self._color_cycle
        elif self.style == "CHASE":
            animation = self._chase[ self.numcolors - 1 ]
        elif self.style == "COMET":
            animation = self._comet[ self.numcolors - 1 ]
        elif self.style == "PULSE":
            animation = self._pulse[ self.numcolors - 1 ]
        elif self.style == "SPARKLE":
            animation = self._sparkle
        elif self.style == "SPARKLE PULSE":
            animation = self._sparkle_pulse
        elif self.style == "RAINBOW":
            animation = self._rainbow
        elif self.style == "RAINBOW CHASE":
            animation = self._rainbow_chase
        elif self.style == "RAINBOW COMET":
            animation = self._rainbow_comet
        elif self.style == "RAINBOW SPARKLE":
            animation = self._rainbow_sparkle
        if animation:
            animation.animate()
        else:
            self.pixels.fill( (0,0,0) )
            self.pixels.show()
        
            