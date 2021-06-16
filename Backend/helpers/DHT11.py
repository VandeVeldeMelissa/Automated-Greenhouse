import time
import board
import adafruit_dht

dht= adafruit_dht.DHT11(board.D4, use_pulseio=False)
 
while True:
    try:
        temperature_c = dht.temperature
        humidity = dht.humidity
        print(f"Temp: {temperature_c}\N{DEGREE SIGN}C") #+/-2C
        print(f"Humidity: {humidity}%") #+/-5%
 
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2)
        continue
    except Exception as error:
        dht.exit()
        raise error
 
    time.sleep(1)