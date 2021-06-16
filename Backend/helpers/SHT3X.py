import smbus
import time
 
bus = smbus.SMBus(1)
time.sleep(1)
sht3x_address = 0x44

#Origineel ging ik een SHT3X gebruiken maar deze blijft maar remote I/O errors krijgen dus gebruik in nu een DHT11

class SHT3X:
    def __init__(self, par_address=sht3x_address):
        self.address = par_address
        self.setup()
    
    def setup(self):
        bus.write_i2c_block_data(0x44, 0x2C, [0x06])
        time.sleep(0.5)

    def read_temperature_and_humidity(self):
        data = bus.read_i2c_block_data(0x44, 0x00, 6)
        temp = -45 + (175 * (data[0] * 256 + data[1]) / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0  
        return [temp, humidity]
    
    def read_temperature(self):
        data = bus.read_i2c_block_data(0x44, 0x00, 6)
        temp = -45+(175*(data[0]*256+data[1])/65535.0) #Datasheet
        return temp
    
    def read_humidity(self):
        data = bus.read_i2c_block_data(0x44, 0x00, 6)
        humidity = 100*(data[3]*256+data[4])/65535.0 #Datasheet
        return humidity

if __name__ == "__main__":
    sht = SHT3X()
    try:
        while(True):
            #print(f"Temp: {sht.read_temperature()}")
            #print(f"Humidity: {sht.read_humidity()}")
            values = sht.read_temperature_and_humidity()
            print(f"Temp: {values[0]} \t Humidity: {values[1]}")
            time.sleep(1)
    except KeyboardInterrupt as e:
        pass
    finally:
        bus.close()
 
 
# SHT31 met libary
# import board
# import busio
# import adafruit_sht31d
# i2c = busio.I2C(board.SCL, board.SDA)
# sensor = adafruit_sht31d.SHT31D(i2c)
# print('Humidity: {0}%'.format(sensor.relative_humidity))
# print('Temperature: {0}C'.format(sensor.temperature))

# Deze werkt soms
# import smbus
# import time
# bus = smbus.SMBus(1)
# bus.write_i2c_block_data(0x44, 0x2C, [0x06])
# time.sleep(0.5)
# data = bus.read_i2c_block_data(0x44, 0x00, 6)
# temp = data[0] * 256 + data[1]
# cTemp = -45 + (175 * temp / 65535.0)
# humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
# print ("Temperature in Celsius is : %.2f C" %cTemp)
# print ("Relative Humidity is : %.2f %%RH" %humidity)