from os import stat
from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    # @staticmethod
    # def read_latest_measurement_sensor(deviceid):
    #     sql = "SELECT h.Value, d.Unit FROM History AS h JOIN Device as d ON d.DeviceID = h.DeviceID WHERE h.DeviceID = %s ORDER BY h.Date DESC LIMIT 1"
    #     params = [deviceid]
    #     return Database.get_one_row(sql, params)

    # @staticmethod
    # def read_all_measurements_sensor(deviceid):
    #     sql = "SELECT h.Value, d.Unit, h.Date FROM History AS h JOIN Device as d ON d.DeviceID = h.DeviceID WHERE h.DeviceID = %s ORDER BY h.Date DESC"
    #     params = [deviceid]
    #     return Database.get_rows(sql, params)

    @staticmethod
    def create_measurement_sensor(device, value):
        sql = "INSERT INTO History (DeviceID, ActionID, Date, Value) VALUES (%s,1,NOW(),%s)"
        params = [device, value]
        return Database.execute_sql(sql, params)
    
    #History sensors
    @staticmethod
    def read_all_sensors():
        sql = "SELECT * FROM Device WHERE Type = 0"
        return Database.get_rows(sql)
    
    #History dates
    @staticmethod
    def read_all_dates_history():
        sql = "SELECT DATE_FORMAT(date,'%d/%m/%Y') AS 'Date', date(Date) AS 'DateFormat' FROM History GROUP BY DATE_FORMAT(date,'%d/%m/%Y')"
        return Database.get_rows(sql)

    #History data between dates from sensor
    @staticmethod
    def read_measurements_sensor_between_dates(device, date1, date2): #both dates inclusive
        sql = "SELECT h.Value, d.Unit, h.Date FROM History AS h JOIN Device as d ON d.DeviceID = h.DeviceID WHERE h.ActionID = 1 AND d.DeviceID = %s AND (Date(h.Date) BETWEEN %s AND %s)"
        params = [device, date1, date2]
        return Database.get_rows(sql, params)
    
    #Management home: add water
    @staticmethod
    def create_action_waterpump(actionid): #2 = start adding water & 3 = stop adding water
        sql = "INSERT INTO History (DeviceID, ActionID, Date, Value) VALUES (7,%s,NOW(),null)"
        params = [actionid]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def read_last_time_watered(): #2 = start adding water & 3 = stop adding water
        sql = "SELECT * FROM History WHERE ActionID = 3 ORDER BY Date DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def create_action_servos(actionid): #4 = open windows & 5 = close windows
        sql = "INSERT INTO History (DeviceID, ActionID, Date, Value) VALUES (8,%s,NOW(),null)"
        params = [actionid]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_state_windows(): #4 = open windows & 5 = close windows
        sql = "SELECT * FROM History WHERE DeviceID = 8 ORDER BY Date DESC LIMIT 1"
        return Database.get_one_row(sql)
    
    @staticmethod
    def update_settings(deviceid, actionid, value): #actionid: 6 = temp, 7 = humidity, 8 = soil moisture & 9 = eco2
        sql = "INSERT INTO History (DeviceID, ActionID, Date, Value) VALUES (%s,%s,NOW(),%s)"
        params = [deviceid, actionid, value]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_settings(actionid): #actionid: 6 = temp, 7 = humidity, 8 = soil moisture & 9 = eco2
        sql = "SELECT * FROM History WHERE ActionID = %s ORDER BY Date DESC LIMIT 1"
        params = [actionid]
        return Database.get_one_row(sql, params)
    
    @staticmethod
    def create_action_pi(actionid): #10 = starts & 11 = stops
        sql = "INSERT INTO History (DeviceID, ActionID, Date, Value) VALUES (9,%s,NOW(),null)"
        params = [actionid]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def read_action_pi(actionid): #10 = starts & 11 = stops
        sql = "SELECT * FROM History WHERE DeviceID = 9 AND ActionID = %s ORDER BY Date DESC LIMIT 1"
        params = [actionid]
        return Database.get_one_row(sql, params)
