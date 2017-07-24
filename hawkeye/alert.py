import logging
from hawkeye.utils.emailer import Emailer
from hawkeye.settings import SMTP_SERVER_SETTINGS

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class Alert:
    def __init__(self, alert_type, limit):
        """Create an alert instance.

        :param alert_type: the metric type
        :param limit: configured limit upon which alerts will be sent in case it's bypassed
        """
        self.type = alert_type
        self.limit = limit
        self.emailer = Emailer(**SMTP_SERVER_SETTINGS)
    def create_message(self, from_addr, to_addrs, value):
        """Create an email message.

        :param from_addr: from address
        :param to_addrs: to address(es)
        :param value: value to be compared to alert.limit
        """
        logging.info('Alert: Created A Message')
        logging.info('subject: {0} Alert\nfrom: {1} \nto: {2}'.format(self.type, from_addr, to_addrs))
        message = 'Subject: [Hawkeye] {0} Alert\nFrom: Hawkeye <{1}>\nTo: Hisham <{2}>\nYour {3} utilization has passed the {4} configured limit. It has reached {5}\n\n\rHappy monitoring!\n\rHawkeye '.format(self.type, from_addr, to_addrs, self.type, self.limit, value)
        return message
    
    def send(self, from_addr, to_addrs, message):
        """Send email message.
        """
        self.emailer.send(from_addr, to_addrs, message)
        logging.info('Alert: message sent!')
