import xmltodict
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from source.client import Client
from source import settings
from source.alert import Alert
import json
import logging

PRIVATE_KEY = RSA.importKey(open(settings.PRIVATE_KEY_PATH).read())
class Hawkeye:
    def __init__(self, xml_config):
        logging.info('Hawkeye: Initializing clients list')
        self.clients = self.parse_config(xml_config)

    def parse_config(self, xml_config):
        logging.info('Hawkeye: Parsing config')
        clients = []
        parsed = xmltodict.parse(xml_config)
        clients_config = parsed['root']['client']
        for client in clients_config:
            ip_address = client['@ip']
            port = int(client['@port'])
            username = client['@username']
            password = client['@password']
            email = client['@mail']
            alerts = []
            for alert_config in client['alert']:
                alerts.append(Alert(alert_config['@type'], alert_config['@limit']))

            clients.append(Client(ip_address, port, username, password, email, alerts))
        return clients

    def run(self):
        logging.info('Hawkeye: Started monitoring')
        for client in self.clients:
            client.connect()
            client.upload_script('monitor.py')
            response = client.execute_script('monitor.py')
            result = client.decrypt(response, PRIVATE_KEY)
            stats_entry = json.loads(result.decode())
            client.save('aDBDriver', stats_entry)
            client.disconnect()

def main():
    xml_config = '''
            <root>
                <client ip="127.0.0.1" port="22" username="sheshtawy" password="Icandoitbefore25" mail="asa@asda.com">

                    <alert type="memory" limit="50%" />
                    <alert type="cpu" limit="20%" />
                </client>

                <client ip="127.0.0.1" port="22" username="sheshtawy" password="Icandoitbefore25" mail="asa@asda3.com">

                    <alert type="memory" limit="50%" />
                    <alert type="cpu" limit="20%" />
                </client>
            </root>
        '''
    hawkeye = Hawkeye(xml_config)
    hawkeye.run()

if __name__ == '__main__':
    main()
