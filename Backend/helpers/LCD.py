from RPi import GPIO
import time

rs = 21
e = 20
lijst_pinnen = [16, 12, 25, 24, 23, 26, 19, 13]


class LCD:
    def __init__(self, par_rs=rs, par_e=e, par_pinnen=lijst_pinnen):
        self.rs = par_rs
        self.e = par_e
        self.pinnen = par_pinnen

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.e, GPIO.OUT)
        for i in lijst_pinnen:
            GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(self.e, GPIO.HIGH)
        self.init_LCD()

    def init_LCD(self):
        self.send_instruction(0x38)
        self.send_instruction(0x0F)
        self.send_instruction(0x01)

    def send_instruction(self, value):
        GPIO.output(self.rs, GPIO.LOW)
        self.set_data_bits(value)
        time.sleep(0.002)

        GPIO.output(self.e, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.e, GPIO.HIGH)
        time.sleep(0.01)

    def send_character(self, value):
        GPIO.output(self.rs, GPIO.HIGH)
        self.set_data_bits(value)
        time.sleep(0.002)

        GPIO.output(self.e, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.e, GPIO.HIGH)

    def set_data_bits(self, value):
        mask = 0b00000001
        for i in range(0, 8):
            pin = self.pinnen[i]
            if value & mask:
                GPIO.output(pin, GPIO.HIGH)
            else:
                GPIO.output(pin, GPIO.LOW)
            mask <<= 1

    def write_message(self, message):
        for char in message[0:16]:
            self.send_character(ord(char))
        for char in message[16:]:
            self.send_instruction(0b00011000)
            self.send_character(ord(char))

    def set_cursor(self, row, col):
        byte = row << 6 | col
        self.send_instruction(byte | 128)

    def clear_display(self):
        self.send_instruction(1)


if __name__ == '__main__':
    try:
        lcd = LCD()
        lcd.init_LCD()
        lcd.write_message("Hallo")
        time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        lcd.clear_display()
        GPIO.cleanup()
