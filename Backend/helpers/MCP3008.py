from RPi import GPIO
import spidev
import time


class MCP3008:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 10**5  # Clockfrequency: 100kHz

    def read_channel(self, channel):
        bytes_uit = [0b00000001, (8 | channel) << 4, 0b00000000]
        bytes_in = self.spi.xfer2(bytes_uit)
        result = ((bytes_in[1] & 3) << 8) | bytes_in[2]
        if channel == 0:  # soil moisture sensor
            return convert_percent(result)
        if channel == 1:  # light intensity
            return convert_percent(result)

    def close_spi(self):
        self.spi.close()


def convert_percent(waarde):
    # soil moisture & light intensity give low values when the moisture/intensity is high
    waarde = (1023 - waarde)
    #0-1023 => 0%-100%
    return round((waarde/1023.0)*100, 2)


if __name__ == "__main__":
    try:
        while(True):
            print(f"Value soil moisture:")
            print(MCP3008().read_channel(0))
            print(f"Value light intensity:")
            print(MCP3008().read_channel(1))
            time.sleep(1)
    except KeyboardInterrupt as e:
        pass
    finally:
        MCP3008().close_spi()
        GPIO.cleanup()
