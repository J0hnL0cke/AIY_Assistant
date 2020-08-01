import time
import aiy.board as board
import threading

def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)

class lights:
    
    led_inst=None
    current_color=None
    
    @classmethod
    def _get_led_inst(cls):
        try:
            cls.led_inst=leds.Leds()
        except:
            #Creating an instance of Leds() sometimes fails when running program at boot.
            #If an instance hasn't been created, try to create one when changing the led color.
            #This should provide some delay to allow the Leds() package to initialize.
            
            cls.led_inst=None
            print("Couldn't initialize leds")
    
    @classmethod
    def init(cls):
        #Have to set this after importing aiy.leds, cannot go in class body
        cls.colors=['off', leds.Color.CYAN, leds.Color.WHITE, leds.Color.PURPLE, leds.Color.YELLOW, leds.Color.BLUE, leds.Color.GREEN, leds.Color.RED]
        cls.names=['off', 'cyan', 'white', 'purple', 'yellow', 'blue', 'green', 'red']
        print('Initializing leds...')
        cls._get_led_inst()
    
    @classmethod
    def button_change(cls, c):
        #Try to initialize if instance doesn't exist
        if cls.led_inst is None:
            print("Trying to create an LED instance")
            cls._get_led_inst()
        
        #If instance exists
        if cls.led_inst is not None:
            print('Changing LED color to', c)
            color=cls.colors[cls.names.index(c)]
            
            if color==cls.current_color:
                print("led is already set to", color)
            elif color=='off':
                cls.led_inst.update(leds.Leds.rgb_off())
            else:
                cls.led_inst.update(leds.Leds.rgb_on(color))
            cls.current_color=color
        else:
            print("Cannot change led color: Leds() not yet initialized.")
        
    @classmethod
    def reset_led(cls):
        #Turn off leds before the program exits so they are not left on
        if not cls.led_inst is None:
            print('Resetting led')
            try:
                cls.button_change('off')
                del cls.led_inst
            except:
                print("When resetting led, another error ocurred:")
                raise

class btn:
    
    stage=0
    
    @classmethod
    def init(cls):
        print('Initializing button...')
        cls.board=board.Board()
        cls.stage=1
        
    @classmethod
    def wait(cls):
        print("Waiting for button press")
        cls.board.button.wait_for_press()
        
    @classmethod
    def clean_up(cls):
        assert cls.stage != 0
        cls.board.button.close()
        print("Cleaned up button handler")
        cls.stage=0
        
import aiy.leds as leds
import time
print("Service started")
lights.init()
lights.button_change("red")
time.sleep(2)
lights.reset_led()
btn.init()
btn.wait()
print("Button pressed")
btn.clean_up()
print("Starting assistant")

#execute the file
execfile("main.py")

#The service should then restart. If not, exit
exit()
