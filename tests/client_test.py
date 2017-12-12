from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import json
import paramiko
from hawkeye import settings
from hawkeye.client import Client
from hawkeye.alert import Alert

class TestClient(object):

    def test_connect(self, client):
        client.connect()
        assert client.is_connected
        assert client.connection is not None

    def test_disconnect(self, client):
        client.connect()
        assert client.is_connected

        client.disconnect()
        assert not client.is_connected

    def test_upload_script(self, client):
        client.connect()
        result = client.upload_script('monitor.py')
        assert isinstance(result, paramiko.sftp_attr.SFTPAttributes)

    def test_execute_script(self, client, cipher):
        client.connect()
        response = client.execute_script('monitor.py')
        stats = cipher.decrypt(response)
        stats_obj = json.loads(stats.decode())
        assert sorted(['cpu', 'memory', 'uptime']) == list(stats_obj.keys())

    def test_save(self, client, db_driver):
        client.connect()
        client.save(db_driver, {
            'cpu': '50',
            'memory': '50',
            'uptime': '1000'
        })
        entry = db_driver.retrieve('hawkeye_db', 'stats', 'stat_id', '3')
        assert set([50, 50, 1000]).issubset(entry)

    def test_decrypt(self, client, cipher):
        message = b'this is a test message'
        private_key = RSA.importKey(open(settings.PRIVATE_KEY_PATH).read())
        public_key = RSA.importKey(
            open(os.path.expanduser('~/.hawkeye/') + 'public_key.pub').read()
            )
        encrypter = PKCS1_OAEP.new(public_key)
        cipher_text = encrypter.encrypt(message)
        assert client.decrypt(cipher_text, private_key) == message
