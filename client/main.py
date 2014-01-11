from apscheduler.scheduler import Scheduler

sched = Scheduler(standalone=True)

@sched.interval_schedule(minutes=1)
def execute_sensors():
	print("Kikoo")

try:
	sched.start()
except KeyboardInterrupt:
	print "Exitting !"
	sched.shutdown(wait=True)
