#import neopixel
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.sequence import AnimationSequence
class Zone:
    pixels = None
    _animation = None
    
    def reset( self, style, color1, color2, color3 ):
        self.__init__( self.pixels, style, color1, color2, color3 )
    
    def hex_to_rgb( self, hex ):
        if hex:
            hex = hex.lstrip('#')
            return tuple( int( hex[i:i+2], 16 ) for i in ( 0, 2, 4 ) )
        return None

    def __init__( self, pixels, style, color1, color2, color3  ):
        self.pixels = pixels
        color1 = self.hex_to_rgb(color1)
        color2 = self.hex_to_rgb(color2)
        color3 = self.hex_to_rgb(color3)

        if style == "SOLID":
            self._animation = Solid(pixels, color = color1 )
        elif style == "BLINK1":
            self._animation = Blink(pixels, speed=0.5, color = color1 )
        elif style == "BLINK2":
            self._animation = AnimationSequence(
                Blink(pixels, speed=0.5, color = color1 ),
                Blink(pixels, speed=0.5, color = color2 ),
                advance_on_cycle_complete = True
            )
        elif style == "BLINK3":
            self._animation = AnimationSequence(
                Blink(pixels, speed=0.5, color = color1 ),
                Blink(pixels, speed=0.5, color = color2 ),
                Blink(pixels, speed=0.5, color = color3 ),
                advance_on_cycle_complete = True
            )
        elif style == "CHASE1":
            self._animation = Chase(pixels, speed=0.1, color = color1, size = 3 )
        elif style == "CHASE2":
            self._animation = AnimationSequence(
                Chase(pixels, speed=0.1, color = color1, size = 3 ),
                Chase(pixels, speed=0.1, color = color2, size = 3 ),
                advance_on_cycle_complete = True
            )
        elif style == "CHASE3":
            self._animation = AnimationSequence(
                Chase(pixels, speed=0.1, color = color1, size = 3 ),
                Chase(pixels, speed=0.1, color = color2, size = 3 ),
                Chase(pixels, speed=0.1, color = color3, size = 3 ),
                advance_on_cycle_complete = True
            )
        elif style == "COMET1":
            self._animation = Comet(pixels, speed=0.01, color = color1, bounce = True )
        elif style == "COMET2":
            self._animation = AnimationSequence(
                Comet(pixels, speed=0.01, color = color1, bounce = True ),
                Comet(pixels, speed=0.01, color = color2, bounce = True ),
                advance_on_cycle_complete = True
            )
        elif style == "COMET3":
            self._animation = AnimationSequence(
                Comet(pixels, speed=0.01, color = color1, bounce = True ),
                Comet(pixels, speed=0.01, color = color2, bounce = True ),
                Comet(pixels, speed=0.01, color = color3, bounce = True ),
                advance_on_cycle_complete = True
            )
        elif style == "PULSE1":
            self._animation = Pulse(pixels, speed=0.1, color = color1 )
        elif style == "PULSE2":
            self._animation = AnimationSequence(
                Pulse(pixels, speed=0.1, color = color1 ),
                Pulse(pixels, speed=0.1, color = color2 ),
                advance_on_cycle_complete = True
            )
        elif style == "PULSE3":
            self._animation = AnimationSequence(
                Pulse(pixels, speed=0.1, color = color1 ),
                Pulse(pixels, speed=0.1, color = color2 ),
                Pulse(pixels, speed=0.1, color = color3 ),
                advance_on_cycle_complete = True
            )
        elif style == "SPARKLE":
            self._animation = Sparkle(pixels, speed=0.05, color = color1 )
        elif style == "SPARKLE PULSE":
            self._animation = SparklePulse(pixels, speed=0.05, color = color1 )
        elif style == "RAINBOW":
            self._animation = Rainbow( pixels, speed = 0.1 )
        elif style == "RAINBOW CHASE":
            self._animation = RainbowChase( pixels, speed=0.1, size=5, spacing=3)
        elif style == "RAINBOW COMET":
            self._animation = RainbowComet( pixels, speed=0.1, tail_length=7, bounce=True)
        elif style == "RAINBOW SPARKLE":
            self._animation = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)
        elif style == "INTRUDER":
            self._animation = Blink(pixels, speed = 0.1, color=(255,0,0))
        
    def process_colors( self ):
        if self._animation:
            self._animation.animate()
        else:
            self.pixels.fill( (0,0,0) )
            self.pixels.show()

            
