class Sensor:
    def __init__(self, conf):
        pass
        
    def sense(self):
        pass

class PingSensor(Sensor):
    def __init__(self, conf):
        self.address = conf["address"]
        Sensor.__init__(self, conf)
        
    def sense(self):
        import subprocess, re
        
        output = subprocess.check_output(["ping", "-q", "-c", "10", self._address])
        lines = output.split("\n")
        res = dict()
        for l in lines:
            if "received" in l:
                m = re.match(r'(\d+) packets received, (\d+) lost')
                if m:
                    received = m[0]
                    lost = m[1]
                    res["packet_total"] = 10
                    res["packet_received"] = received
                    res["packet_lost"] = lost
            elif "rtt" in l:
                m = re.search(r'(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)')
                if m:
                    min_time = m[0]
                    avg_time = m[1]
                    max_time = m[2]
                    res["min_time"] = min_time
                    res["avg_time"] = avg_time
                    res["max_time"] = max_time
        return res
        
class SpeedSensor(Sensor):
    def __init__(self, conf):
        self._address = conf["address"]
        Sensor.__init__(self, conf)
        
    def sense(self):
        pass