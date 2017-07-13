class Alert:
    def __init__(self, alert_type, limit):
        self.type = alert_type
        self.limit = limit

    def create_message(self, from_addr, to_addrs, value):
        """Create an email message.

        :param from_addr: from address
        :param to_addrs: to address(es)
        :param value: value to be compared to alert.limit
        """
        print('Created a message:')
        print ('subject: {0} Alert\nfrom: {1} \nto: {2}'.format(self.type, from_addr, to_addrs))

    def send(self, message):
        """Send email message.
        """
        print('message sent!')
