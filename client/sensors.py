class Sensor:
    def __init__(self, conf):
        pass
        
    def sense(self):
        pass

class PingSensor(Sensor):
    def __init__(self, address=None, **kwargs):
        self._address = address
        Sensor.__init__(self, kwargs)
        
    def sense(self):
        import subprocess, re
        
        res = dict()
        process = subprocess.Popen(["ping", "-q", "-c", "10", self._address], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = process.stdout
        for l in stdout.readline():
            print("ping> ", l)
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
        process.wait()
        if process.returncode <> 0:
            res["failed"] = True
        return res
        
class SpeedSensor(Sensor):
    def __init__(self, address=None, **kwargs):
        self._address = address
        Sensor.__init__(self, **kwargs)
        
    def sense(self):
        pass
