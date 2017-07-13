import smtplib

class Emailer:
    def __init__(self, host, port, protocol='SMTP'):
        self.host = host
        self.port = port
        self.protocol = protocol

    def _connect(self):
        if self.protocol == 'SMTP':
            conn = smtplib.SMTP(host=self.host, port=self.port)
            conn.ehlo()
            conn.connect(host=self.host, port=self.port)
            conn.ehlo()
            return conn

    def send(self, from_addr, to_addrs, message):
        conn = self._connect()
        conn.sendmail(from_addr, to_addrs, message)
    