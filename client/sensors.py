class Sensor:
    def __init__(self, conf):
        pass
        
    def sense(self):
        pass

class SensorManager:
    def __init__(self, baseAddress, sensor):
	from hammock import Hammock

        self._service = Hammock(baseAddress, append_slash=True).api('v1').ticks
	self._sensor = sensor

    def run(self):
	from datetime import datetime
	import json

	result = self._sensor.sense()
	tick = dict()
	tick['tick_date'] = datetime.now().isoformat()
	tick['type'] = self._sensor.__class__.__name__
	tick['data'] = result
	response = self._service.POST(headers={'content-type': 'application/json'}, data=json.dumps(tick))

class PingSensor(Sensor):
    def __init__(self, address=None, **kwargs):
        self._address = address
        Sensor.__init__(self, kwargs)
        
    def sense(self):
        import subprocess, re
        
        res = dict()
        process = subprocess.Popen(["ping", "-q", "-c", "10", self._address], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for l in process.stdout:
            if "received" in l:
                m = re.match(r'(\d+) packets transmitted, (\d+) received', l)
                if m:
                    g = m.groups()
                    transmitted = int(g[0])
                    received = int(g[1])
                    res["packet_total"] = transmitted
                    res["packet_received"] = received
                    res["packet_lost"] = transmitted - received
            elif "rtt" in l:
                m = re.search(r'(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)', l)
                if m:
                    g = m.groups()
                    min_time = float(g[0])
                    avg_time = float(g[1])
                    max_time = float(g[2])
                    res["min_time"] = min_time
                    res["avg_time"] = avg_time
                    res["max_time"] = max_time
            elif "Destination Host Unreachable" in l:
                res["reason"] = "unreachable"
        process.wait()
        if process.returncode <> 0:
            res["failed"] = True
        return res

class DnsSpeedSensor(Sensor):
    def __init__(self, address=None, **kwargs):
        self._address = address
        Sensor.__init__(self, kwargs)

    def sense(self):
        import socket, time

        res = dict()
        t = time.time()
        try:
            socket.getaddrinfo(self._address, None)
            res["result"] = "success"
        except socket.gaierror:
            res["result"] = "error"

        res["time"] = time.time() - t
        return res
        
class SpeedSensor(Sensor):
    def __init__(self, address=None, **kwargs):
        self._address = address
        Sensor.__init__(self, kwargs)
        
    def sense(self):
	import requests, time

	res = dict()
	size = 0
	t = time.time()
	r = requests.get(self._address, stream=True)

	if r.status_code == 200:
		for chunk in r.iter_content(chunk_size=512):
			size += len(chunk)
		res["size"] = size
	else:
		res["failed"] = True

	res["time"] = time.time() - t
	return res
