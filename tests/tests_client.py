import unittest
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import paramiko
import json
import os

from source import settings
from source.client import Client
from source.alert import Alert

class ClientTests(unittest.TestCase):
    
    def setUp(self):
        self.private_key = RSA.importKey(open(settings.PRIVATE_KEY_PATH).read())
        self.cipher = PKCS1_OAEP.new(self.private_key)
        self.public_key = RSA.importKey(
            open(os.path.expanduser('~/.hawkeye/') + 'public_key.pub').read()
            )
        self.sample_client = Client(
            '127.0.0.1',
            port=22,
            username='sheshtawy',
            password='Icandoitbefore25',
            mail='hisham.elsheshtawy@gmail.com',
            alerts=[
                Alert(alert_type='memory', limit='20'),
                Alert(alert_type='cpu', limit='30')
            ]  
        )

    def testConnectSucessfully(self):
        self.sample_client.connect()
        self.assertTrue(self.sample_client.is_connected, 'the client is not connected')
        self.assertTrue(isinstance(self.sample_client.connection, paramiko.client.SSHClient))

    def testDisconnectSuccessfully(self):
        self.sample_client.disconnect()
        self.assertFalse(self.sample_client.is_connected)

    def testUploadScript(self):
        self.sample_client.connect()
        result = self.sample_client.upload_script('monitor.py')
        self.assertTrue(isinstance(result, paramiko.sftp_attr.SFTPAttributes))

    def testExecuteScript(self):
        self.sample_client.connect()
        response = self.sample_client.execute_script('monitor.py')
        stats = self.cipher.decrypt(response)
        stats_obj = json.loads(stats.decode())
        self.assertListEqual(
            sorted(['cpu', 'memory', 'uptime']),
            sorted(list(stats_obj.keys()))
        )

    def testSave(self):
        pass

    def testDecrypt(self):
        sample_message = b'this is a sample message'
        encrypter = PKCS1_OAEP.new(self.public_key)
        cipher_text = encrypter.encrypt(sample_message)
        result = self.sample_client.decrypt(cipher_text, self.private_key)
        self.assertEqual(sample_message, result)


    def testCheckAlerts(self):
        pass


def main():
    unittest.main()
    
if __name__ == "__main__":
    main()
