import sensors

d = dict()
d["address"] = "http://python.org"
sensor = sensors.SpeedSensor(**d)
print(sensor.sense())
