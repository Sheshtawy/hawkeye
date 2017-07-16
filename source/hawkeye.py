import xmltodict
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from source.client import Client
from source import settings
from source.alert import Alert
from source.utils.db_drivers.postgres_driver import PostgresDriver
import json
import logging
import argparse

PRIVATE_KEY = RSA.importKey(open(settings.PRIVATE_KEY_PATH).read())
class Hawkeye:
    def __init__(self, xml_config):
        logging.info('Hawkeye: Initializing clients list')
        self.db_driver = PostgresDriver(**settings.DB_CREDENTIALS)
        self.clients = self._parse_config(xml_config)

    def _parse_config(self, xml_config):
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
            alerts_db_array = []

            for alert_config in client['alert']:
                alerts.append(Alert(alert_config['@type'], alert_config['@limit']))
                alerts_db_array.append([alert_config['@type'], alert_config['@limit']])
                
            client_instance = self.db_driver.retrieve('hawkeye_db', 'clients', 'ip_address', ip_address)
            print('client_instance', client_instance)
            if client_instance is None:
                data = {
                    'ip_address': ip_address,
                    'port': port,
                    'username': username,
                    'password': password,
                    'email': email,
                    'alerts': alerts_db_array
                }
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
            client.save(self.db_driver, stats_entry)
            client.check_alerts(stats_entry)
            client.disconnect()
            
def main():
    """Run the module."""
    parser = argparse.ArgumentParser(
        description='A tool for monitoring machines in an intranet.'
    )
    parser.add_argument(
        'xml_config_path', 
        help="path to xml config file for nodes you want to monitor"
    )
    args = parser.parse_args()
    xml_config = open(args.xml_config_path, 'r').read()
    hawkeye = Hawkeye(xml_config)
    hawkeye.run()

if __name__ == '__main__':
    main()
