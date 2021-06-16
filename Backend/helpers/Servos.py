from RPi import GPIO
import time

servo1 = 27
servo2 = 17


class Servos:
    def __init__(self, pin1=servo1, pin2=servo2, freq=50):
        self.pin1 = pin1
        self.pin2 = pin2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)
        self.pwm1 = GPIO.PWM(pin1, freq)
        self.pwm2 = GPIO.PWM(pin2, freq)

    def start(self):
        self.pwm1.start(0)
        self.pwm2.start(0)

    def set_angle(self, angle, servo):
        duty = angle / 18 + 3
        if servo == 1:
            self.pwm1.ChangeDutyCycle(duty)
        if servo == 2:
            self.pwm2.ChangeDutyCycle(duty)
        time.sleep(1)

    def change_frequency(self, freq):
        self.pwm1.ChangeFrequency(freq)
        self.pwm1.ChangeFrequency(freq)

    def stop(self):
        self.pwm1.stop()
        self.pwm2.stop()


if __name__ == "__main__":
    s = Servos()
    s.start()
    try:
        s.set_angle(10, 2) #servo 2 100 graden toe en 10 graden open
        s.set_angle(30, 1) #servo 1 130 graden toe en 30 graden open 
        s.stop()
    except KeyboardInterrupt as e:
        print(e)
    finally:
        GPIO.cleanup()
