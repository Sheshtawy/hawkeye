import os
from datetime import datetime
import base64

import psutil
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import json

class Monitor:
    def __init__(self, key_path):
        self._key_path = key_path

    def get_stats(self):
        cpu_utilization = self.get_cpu_utilization()
        memory_utilization = self.get_memory_utilization()
        total_uptime = self.get_total_uptime()

        data = {
            'cpu': cpu_utilization,
            'memory': memory_utilization,
            'uptime': total_uptime
        }
        message = json.dumps(data).encode()
        return self._encrypt(message)

    def get_cpu_utilization(self):
        return psutil.cpu_percent()

    def get_memory_utilization(self):
        return psutil.virtual_memory().percent

    def get_total_uptime(self):
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        now = datetime.now()
        total_uptime = now - boot_time
        total_uptime = total_uptime.total_seconds()
        return total_uptime

    def _encrypt(self, message):
        key = RSA.importKey(open(self._key_path).read())
        cipher = PKCS1_OAEP.new(key)
        encrypted_response = cipher.encrypt(message)
        return base64.b64encode(encrypted_response)



def main():
    public_key = os.path.expanduser('~/.hawkeye/') + 'public_key.pub'
    monitor = Monitor(public_key)
    return monitor.get_stats()


if __name__ == '__main__':
    import sys
    data = main()
    sys.stdout.write(str(data))
