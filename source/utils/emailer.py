import smtplib
import logging

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class Emailer:
    """A class to help send SMTP emails.
    """

    def __init__(self, default_protocol='SMTP', **kwargs):
        """Create an emailer instance

        :param default_protocol: default protocol to use in case there's no protocol provided
        :param host: Email server host
        :param port: Email server open port
        :param str username: username to authenticate to the email server
        :param password: password to autehnticate to the email server
        """
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.username = kwargs['username']
        self.password = kwargs['password']
        try:
            self.protocol = kwargs['protocol'] or default_protocol
        except KeyError:
            self.protocol = default_protocol

    def _connect(self):
        if self.protocol == 'SMTP':
            conn = smtplib.SMTP(host=self.host, port=self.port)
            return conn

    def send(self, from_addr, to_addrs, message):
        """Send an email notification."""
        try:
            conn = self._connect()
            conn.ehlo()
            conn.starttls()
            conn.login(self.username, self.password)
            conn.ehlo()
            conn.sendmail(from_addr, to_addrs, message)
            conn.close()
        except Exception as unknown_error:
            logging.info('Emailer: Something went wrong with {0}'.format(self.host))
            logging.info(unknown_error)
