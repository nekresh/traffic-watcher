from apscheduler.scheduler import Scheduler
import sensors

sched = Scheduler(standalone=True)

baseAddress = 'http://localhost:8000'
config = [
	{'type': 'PingSensor', 'configuration': {'address': 'ns-server.epita.fr'}},
	{'type': 'DnsSpeedSensor', 'configuration': {'address': 'ns-server.epita.fr'}},
	{'type': 'SpeedSensor', 'configuration': {'address': 'http://ipv4.download.thinkbroadband.com/5MB.zip'}},
]

@sched.interval_schedule(minutes=1)
def execute_sensors():
	for c in config:
		sensorType = getattr(sensors, c['type'])
		sensor = sensorType(**c['configuration'])
		manager = sensors.SensorManager(baseAddress, sensor)
		manager.run()

try:
	sched.start()
	pass
except KeyboardInterrupt:
	print "Exitting !"
	sched.shutdown(wait=True)
