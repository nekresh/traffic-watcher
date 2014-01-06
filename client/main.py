import sensors

d = dict()
d["address"] = "ns-server.epita.fr"
sensor = sensors.PingSensor(**d)
print(sensor.sense())
