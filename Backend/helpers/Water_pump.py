from RPi import GPIO

motor = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor, GPIO.OUT)

try:
    while True:
        GPIO.output(motor, GPIO.HIGH)
except KeyboardInterrupt as e:
    print(e)
    GPIO.output(motor, GPIO.LOW)
finally:
    GPIO.cleanup()
    print("Script is gestopt!")