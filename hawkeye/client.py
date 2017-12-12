import os
import paramiko
from hawkeye import utils
import base64
from Crypto.Cipher import PKCS1_OAEP
import logging

from hawkeye.settings import SMTP_SENDER_EMAIL

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class Client:
    """A Class that represents a Client node in an intranet."""
    def __init__(self, ip_address, port, username, password, mail, alerts):
        self.is_connected = False
        self.connection = None
        self.ip_address = ip_address
        self.port = port
        self.username = username
        self.password = password
        self.email = mail
        self.alerts = alerts

    def connect(self):
        """Connect to the client."""
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.ip_address, port=self.port, username=self.username, password=self.password)
        self.is_connected = True
        self.connection = ssh_client
        logging.info('Client(%s): connected successfully', self.ip_address)

    def disconnect(self):
        """Disconnect from the client if connected."""
        if self.connection and self.is_connected:
            self.connection.close()
            self.is_connected = False
            logging.info('Client(%s): Connection closed', self.ip_address)

    def upload_script(self, script_name):
        """Upload a script to the client.
        
        It creates a subdirectory in the client's home directory
        then uploads the script to it
        :param script_name: name of the script to be executed assuming it resides in ./scripts
        """
        sftp_client = self.connection.open_sftp()
        sftp_client.chdir(os.path.expanduser('~'))
        if not ('.hawkeye' in sftp_client.listdir()):
            sftp_client.mkdir('.hawkeye')
        local_path = os.getcwd() + '/scripts/{0}'.format(script_name)
        remote_path = './.hawkeye/{0}'.format(script_name)
        logging.info('Client(%s): Uploaded %s script', self.ip_address, script_name)
        return sftp_client.put(local_path, remote_path)

    def execute_script(self, script_name):
        """Execute a script that has been already uploaded to the client.
     
        :param script_name: name of the script to be executed
        """
        cmds = [
            'cd ~',
            'cd ~/.hawkeye/',
            'source env/bin/activate',
            'python {0}'.format(script_name),
        ]
        stdin, stdout, stderr = self.connection.exec_command(' ; '.join(cmds))
        response = stdout.readline()
        response = response[2:]
        response = base64.b64decode(response)
        # a new stats_enty
        logging.info('Client(%s): %s script executed', self.ip_address, script_name)
        return response

    def save(self, db_driver, stats_entry):
        """Save stats_entry to database.

        :param db_driver: DBDriver instance connected to a database
        :param stats_entry: stats_entry retrieved from the client
        """
        logging.info('Client(%s): stats_entry %s', self.ip_address, stats_entry)
        client = db_driver.retrieve('hawkeye_db', 'clients', 'ip_address', self.ip_address)
        stats_entry['client_id'] = client[0]
        db_driver.create('hawkeye_db', 'stats', stats_entry)
        logging.info('Client(%s): stats entry has been saved to DB', self.ip_address)

    def decrypt(self, cipher_text, key):
        """Decrypts an encrypted message.
       
        It uses PKCS1_OAEP protocol (assymmetric encryption/decryption)
        :param cipher_text: the encrypted message
        :param key: RSA private key to decrypt the message
        :returns: decrypted_message
        """
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(cipher_text)

    def check_alerts(self, stats_entry):
        """Check if a stats entry met any alert limit.
       
        In case a limit is met or bypassed an email will be sent
        to the email address associated with the client
        :param stats_entry: stats_entry retrieved from the client
        """
        for alert in self.alerts:
            if stats_entry[alert.type] >= float(alert.limit[:-1]):
                message = alert.create_message(SMTP_SENDER_EMAIL, self.email, stats_entry[alert.type])
                alert.send(SMTP_SENDER_EMAIL, [self.email], message)
