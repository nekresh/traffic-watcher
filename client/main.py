import sensors

d = dict()
d["address"] = "ns-server.epita.fr"
sensor = sensors.DnsSpeedSensor(**d)
print(sensor.sense())
