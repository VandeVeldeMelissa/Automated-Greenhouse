import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_ccs811

i2c = I2C(1)  # uses board.SCL and board.SDA
ccs811 = adafruit_ccs811.CCS811(i2c)

# Wait for the sensor to be ready
# while not ccs811.data_ready:
#     pass

while True:
    co2 = ccs811.eco2
    #The equivalent CO2 (eCO2) output range for CCS811 is from 400ppm up to 29206ppm.
    print(f"CO2: {co2}")
    time.sleep(0.5)