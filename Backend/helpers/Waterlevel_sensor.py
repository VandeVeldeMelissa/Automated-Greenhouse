from RPi import GPIO
import time

pin_waterlvl = 22


class Waterlevel_sensor:
    def __init__(self, pin=pin_waterlvl, bouncetime=200):
        self.pin = pin
        self.bouncetime = bouncetime

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)

    @property
    def pressed(self):
        pressed = GPIO.input(self.pin)
        return not pressed

    def on_press(self, call_method):
        GPIO.add_event_detect(self.pin, GPIO.FALLING,
                              call_method, bouncetime=self.bouncetime)

    def on_release(self, call_method):
        GPIO.add_event_detect(self.pin, GPIO.RISING,
                              call_method, bouncetime=self.bouncetime)
    
    def on_both(self, call_method):
        GPIO.add_event_detect(self.pin, GPIO.BOTH,
                              call_method, bouncetime=self.bouncetime)

def print_both(pin):
    if GPIO.input(waterlvl.pin) == 1:
        print("Water added")
    else:
        print("Water level LOW")

if __name__ == "__main__":
    waterlvl = Waterlevel_sensor()
    waterlvl.on_both(print_both)
    state_waterlvl_start = GPIO.input(waterlvl.pin)
    if state_waterlvl_start == 1:
        print("water level high")
    else:
        print("water level low")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        GPIO.cleanup()
