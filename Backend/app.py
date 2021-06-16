import time
from RPi import GPIO
from flask.wrappers import Request
from helpers.MCP3008 import MCP3008
from helpers.Waterlevel_sensor import Waterlevel_sensor
from helpers.Servos import Servos
from helpers.LCD import LCD
from subprocess import check_output
import threading
import board
import adafruit_ccs811
import adafruit_dht
from subprocess import call

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, json, jsonify, request
from repositories.DataRepository import DataRepository

# Code Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'MaErLaM1708cm'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True,
                    engineio_logger=True, async_mode="gevent", ping_timeout=1)

CORS(app)

# Code hardware
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

waterlvl = Waterlevel_sensor()
mcp = MCP3008()
# i2c = board.I2C()
# ccs811 = adafruit_ccs811.CCS811(i2c)
dht = adafruit_dht.DHT11(board.D4, use_pulseio=False)

motor = 6
GPIO.setup(motor, GPIO.OUT)

servos = Servos()
lcd = LCD()
lcd.init_LCD()
lcd.clear_display()
ips = str(check_output(['hostname', '--all-ip-addresses']))
ips = ips.replace('b\'','')
list_ips = ips.split()
lcd.write_message(list_ips[0])
lcd.set_cursor(1,0x00)
lcd.write_message(list_ips[1])

#Standard settings
set_temperature = 28
set_humidity = 60
set_soil_moisture = 25
set_eco2 = 450

#Read values latest settings
try:
    set_temperature = DataRepository.read_settings(6)['Value']
    set_humidity = DataRepository.read_settings(7)['Value']
    set_soil_moisture = DataRepository.read_settings(8)['Value']
    set_eco2 = DataRepository.read_settings(9)['Value']
except TypeError:
    print('No settings found in database')

def check_waterlvl_start(state_waterlvl_start):
    if state_waterlvl_start == 1:
        print("Water level high")
        DataRepository.create_measurement_sensor(2, 1)
        socketio.emit('B2F_waterlvl_notification', {'water_level': 1})  # waterlvl OK
    else:
        print("Water level LOW!")
        DataRepository.create_measurement_sensor(2, 0)
        socketio.emit('B2F_waterlvl_notification', {'water_level': 0})  # waterlvl NOT OK

def notification_waterlvl(pin):
    if GPIO.input(waterlvl.pin) == 1:  # Floater goes up
        print("*** WATER LEVEL OK ***")
        DataRepository.create_measurement_sensor(2, 1)
        socketio.emit('B2F_waterlvl_notification', {'water_level': 1})  # waterlvl OK
    else:  # Floater goes down
        print("*** WATER LEVEL LOW ***")
        DataRepository.create_measurement_sensor(2, 0)
        socketio.emit('B2F_waterlvl_notification', {'water_level': 0})  # waterlvl NOT OK

waterlvl.on_both(notification_waterlvl)

def read_soil_moisture():
    global current_soil_moisture
    while True:
        value_soil = mcp.read_channel(0)
        dict_soil = {'Value':value_soil, 'Unit':'%'}
        current_soil_moisture = value_soil
        # DataRepository.create_measurement_sensor(1, value_soil) #DeviceID = 1
        socketio.emit('B2F_latest_data_sensor_soil', {'sensor': dict_soil})
        time.sleep(1)

def read_eCO2():
    global current_eco2
    while True:
        try:
            value_eCO2 = ccs811.eco2
            dict_eco2 = {'Value':value_eCO2, 'Unit':'ppm'}
            if value_eCO2 is not None and value_eCO2 >= 400 and value_eCO2 <= 29206: #Output range: fom 400ppm up to 29206ppm
                current_eco2 = value_eCO2
                # DataRepository.create_measurement_sensor(5, value_eCO2) #DeviceID = 5
                # latest_data_eCO2 = DataRepository.read_latest_measurement_sensor(5)
                socketio.emit('B2F_latest_data_sensor_eCO2', {'sensor': dict_eco2})
            time.sleep(1)
        except ValueError as v:
            print(v)
            continue
        except RuntimeError as r:
            print(r)
            continue

def read_temperature():
    global current_temperature
    while True:
        try:
            value_temp = dht.temperature
            dict_temp = {'Value':value_temp, 'Unit':'°C'}
            current_temperature = value_temp
            # DataRepository.create_measurement_sensor(3, value_temp) #DeviceID = 3
            # latest_data_temp = DataRepository.read_latest_measurement_sensor(3)
            socketio.emit('B2F_latest_data_sensor_temp', {'sensor': dict_temp})
            time.sleep(1)
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2)
            continue
        except Exception as error:
            dht.exit()
            raise error

def read_humidity():
    global current_humidity
    while True:
        try:
            value_humidity = dht.humidity
            dict_humidity = {'Value':value_humidity, 'Unit':'%'}
            current_humidity = value_humidity
            # DataRepository.create_measurement_sensor(4, value_humidity) #DeviceID = 4
            # latest_data_humidity = DataRepository.read_latest_measurement_sensor(4)
            socketio.emit('B2F_latest_data_sensor_humidity', {'sensor': dict_humidity})
            time.sleep(1)
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2)
            continue
        except Exception as error:
            dht.exit()
            raise error

def read_light_intensity():
    global current_light_intensity
    while True:
        value_light = mcp.read_channel(1)
        dict_light = {'Value':value_light, 'Unit':'%'}
        current_light_intensity = value_light
        # DataRepository.create_measurement_sensor(6, value_light) #DeviceID = 6
        # latest_data_light = DataRepository.read_latest_measurement_sensor(6)
        socketio.emit('B2F_latest_data_sensor_light', {'sensor': dict_light})
        time.sleep(1)

def activate_water_pump():
    if GPIO.input(motor) == 0:
        GPIO.output(motor, GPIO.HIGH)
        DataRepository.create_action_waterpump(2) #Start adding water
    else: 
        GPIO.output(motor, GPIO.LOW)
        DataRepository.create_action_waterpump(3) #Stop adding water

def activate_servos():
    state_windows = DataRepository.read_state_windows()
    servos.change_frequency(50)
    servos.start()
    if state_windows['ActionID'] == 4: #Currently open
        servos.set_angle(100, 2)
        servos.set_angle(130, 1)
        DataRepository.create_action_servos(5) #Close windows
    if state_windows['ActionID'] == 5: #Currently closed
        servos.set_angle(10, 2)
        servos.set_angle(30, 1)
        DataRepository.create_action_servos(4) #Open windows
    servos.stop()

def send_to_database():
    while True:
        DataRepository.create_measurement_sensor(1, current_soil_moisture)
        # DataRepository.create_measurement_sensor(5, current_eco2)
        DataRepository.create_measurement_sensor(3, current_temperature)
        DataRepository.create_measurement_sensor(4, current_humidity)
        DataRepository.create_measurement_sensor(6, current_light_intensity)
        time.sleep(60*15)

def automation():
    #Check state windows at start
    state_windows = DataRepository.read_state_windows()
    if state_windows['ActionID'] == 4: #Currently open
        state_windows_auto = 1
    if state_windows['ActionID'] == 5: #Currently closed
        state_windows_auto = 0
    state_water_auto = 0
    hysteresis = 1

    while True:
        #Importance temperature
        difference_temp =  abs(set_temperature - current_temperature)
        importance_temperature = 0
        if importance_temperature == 0:
            if difference_temp >= (2 + hysteresis/2):
                importance_temperature = 1
        if importance_temperature == 1:
            if difference_temp >= (4 + hysteresis/2):
                importance_temperature = 2
            elif difference_temp <= (2 - hysteresis/2):
                importance_temperature = 0
        if importance_temperature == 2:
            if difference_temp >= (6 + hysteresis/2):
                importance_temperature = 3
            elif difference_temp <= (4 - hysteresis/2):
                importance_temperature = 1
        if importance_temperature == 3:
            if difference_temp <= (6 - hysteresis/2):
                importance_temperature = 2
            elif difference_temp >= (8-hysteresis/2):
                importance_temperature = 4
        if importance_temperature == 4:
            if difference_temp <= (8 - hysteresis/2):
                importance_temperature = 3
        
        #Importance humidity
        difference_humidity =  abs(set_temperature - current_temperature)
        importance_humidity = 0
        if importance_humidity == 0:
            if difference_humidity >= (5 + hysteresis/2):
                importance_humidity = 1
        if importance_humidity == 1:
            if difference_humidity >= (10 + hysteresis/2):
                importance_humidity = 2
            elif difference_humidity <= (5 - hysteresis/2):
                importance_humidity = 0
        if importance_humidity == 2:
            if difference_humidity >= (15 + hysteresis/2):
                importance_humidity = 3
            elif difference_humidity <= (10 - hysteresis/2):
                importance_humidity = 1
        if importance_humidity == 3:
            if difference_humidity <= (15 - hysteresis/2):
                importance_humidity = 2
            elif difference_humidity >= (20 - hysteresis/2):
                importance_humidity = 4
        if importance_humidity == 4:
            if difference_humidity <= (20 - hysteresis/2):
                importance_humidity = 3

        #Windows open/close automaticly depending on temperature & humidity
        if importance_temperature >= importance_humidity:
            if current_temperature - set_temperature > 2 and state_windows_auto == 0:
                servos.change_frequency(50)
                servos.start()
                servos.set_angle(75)
                DataRepository.create_action_servos(4) #Open windows
                state_windows_auto = 1
                servos.stop()
                print(f'verschil temp: {current_temperature - set_temperature}')
            elif current_temperature - set_temperature <= -1 and state_windows_auto == 1:
                servos.change_frequency(50)
                servos.start()
                servos.set_angle(0)
                DataRepository.create_action_servos(5) #Close windows
                state_windows_auto = 0
                servos.stop()
                print(f'verschil temp: {current_temperature - set_temperature}')
        elif importance_humidity > importance_temperature:
            if current_humidity - set_humidity > 5 and state_windows_auto == 0:
                servos.change_frequency(50)
                servos.start()
                servos.set_angle(75)
                DataRepository.create_action_servos(4) #Open windows
                socketio.send('B2F_change_windows')
                state_windows_auto = 1
                servos.stop()
                print(f'verschil hum: {current_humidity - set_humidity}')
            elif current_humidity - set_humidity <= -7 and state_windows_auto == 1:
                servos.change_frequency(50)
                servos.start()
                servos.set_angle(0)
                DataRepository.create_action_servos(5) #Close windows
                socketio.send('B2F_change_windows')
                state_windows_auto = 0
                servos.stop()
                print(f'verschil hum: {current_humidity - set_humidity}')
        
        #Adds water automaticly when soil gets to dry
        if current_soil_moisture < (set_soil_moisture-7) and state_water_auto == 0:
            GPIO.output(motor, GPIO.HIGH)
            DataRepository.create_action_waterpump(2) #Start adding water
            state_water_auto = 1
        elif current_soil_moisture < (set_soil_moisture-3) and state_water_auto == 1:  #Because the water drips a while after the motor stops
            GPIO.output(motor, GPIO.LOW)
            DataRepository.create_action_waterpump(3) #Stop adding water
            state_water_auto = 0

        time.sleep(1)

thread1 = threading.Thread(target=read_soil_moisture)
#thread2 = threading.Thread(target=read_eCO2)
thread3 = threading.Thread(target=read_temperature)
thread4 = threading.Thread(target=read_humidity)
thread5 = threading.Thread(target=read_light_intensity)
thread6 = threading.Timer(15, send_to_database)
thread7 = threading.Timer(15, automation)

thread1.start()
#thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()

# Custom endpoint
endpoint = '/api/v1'

# Routes

@app.route('/')
def index():
    return "Please visit api route"


@app.route(endpoint + '/')
def api():
    return "Welcome to API"

@app.route(endpoint + '/measurements/<id>/<date1>/<date2>', methods=['GET'])
def read_measurements_dates(id, date1, date2):
    data = DataRepository.read_measurements_sensor_between_dates(id, date1, date2)
    new_data = []
    for x in data:
        measurement = {
            "Value": x['Value'],
            "Unit": x["Unit"],
            "Date": x['Date'].strftime("%Y-%m-%d %H:%M:%S")
        }
        new_data.append(measurement)
    if new_data is not None:
        return jsonify(measurements=new_data), 200
    else:
        return jsonify(status="error"), 404

@app.route(endpoint + '/sensors', methods=['GET'])
def read_sensors():
    data = DataRepository.read_all_sensors()
    if data is not None:
        return jsonify(sensors=data), 200
    else:
        return jsonify(status="error"), 404

@app.route(endpoint + '/dates', methods=['GET'])
def read_dates():
    data = DataRepository.read_all_dates_history()
    new_data = []
    for x in data:
        date = {
            "Date": x['Date'],
            "DateFormat": x['DateFormat'].strftime("%Y-%m-%d"),
        }
        new_data.append(date)
    if data is not None:
        return jsonify(dates=new_data), 200
    else:
        return jsonify(status="error"), 404

@app.route(endpoint + '/watered', methods=['GET'])
def read_last_time_watered():
    data = DataRepository.read_last_time_watered()
    if data is not None:
        return jsonify(data), 200
    else:
        return jsonify(status="error"), 404

@app.route(endpoint + '/windows', methods=['GET'])
def read_windows_state():
    data = DataRepository.read_state_windows()
    if data is not None:
        return jsonify(data), 200
    else:
        return jsonify(status="error"), 404

@app.route(endpoint + '/settings', methods=['GET','PUT'])
def update_settings():
    global set_temperature
    global set_soil_moisture
    global set_humidity
    global set_eco2
    if request.method == 'GET':
        temperature = DataRepository.read_settings(6)
        humidity = DataRepository.read_settings(7)
        soil_moisture = DataRepository.read_settings(8)
        eco2 = DataRepository.read_settings(9)
        data = [temperature, humidity, soil_moisture, eco2]
        if data is not None:
            return jsonify(settings=data), 200
        else:
            return jsonify(status="error"), 404
    if request.method == 'PUT':
        data = DataRepository.json_or_formdata(request)
        temp = DataRepository.update_settings(3, 6, data['temperature'])
        hum = DataRepository.update_settings(4, 7, data['humidity'])
        soil = DataRepository.update_settings(1, 8, data['soil_moisture'])
        co2 = DataRepository.update_settings(5, 9, data['eco2'])
        set_temperature = float(data['temperature'])
        set_humidity = float(data['humidity'])
        set_soil_moisture = float(data['soil_moisture'])
        set_eco2 = float(data['eco2'])
        setting_values = [temp, hum, soil, co2]
        if setting_values is not None:
            return jsonify(message="Record(s) updated!")
        else:
            return jsonify(message="nothing to update")

@app.route(endpoint + '/startup', methods=['GET'])
def read_startup_backend():
    if request.method == 'GET':
        data = DataRepository.read_action_pi(10)
        if data is not None:
            return jsonify(data), 200
        else:
            return jsonify(status="error"), 404

# Socket io
@socketio.on('connect')
def initial_connection():
    print('A new client connects')
    check_waterlvl_start(GPIO.input(waterlvl.pin)) #Checks water level at start

@socketio.on('message')
def listen_to_button_water(msg):
    if msg == 'F2B_add_water':
        activate_water_pump()
    if msg == 'F2B_change_windows':
        activate_servos()
    if msg == 'F2B_turn_off':
        call("echo W8w00rd | sudo -S shutdown -h now", shell=True)

if __name__ == '__main__':
    try:
        DataRepository.create_action_pi(10)
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        DataRepository.create_action_pi(11)
        GPIO.output(motor, GPIO.LOW)
        GPIO.cleanup()