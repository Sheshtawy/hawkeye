import pytest
from hawkeye.alert import Alert
from hawkeye.client import Client
from hawkeye import settings
import pytest
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import paramiko
import os

cpu_alert = Alert('cpu', 20)
memory_alert = Alert('memory', 20)

@pytest.fixture
def client():
    """Sample client in the network
    """
    private_key = RSA.importKey(open(settings.PRIVATE_KEY_PATH).read())
    cipher = PKCS1_OAEP.new(private_key)
    public_key = RSA.importKey(
        open(os.path.expanduser('~/.hawkeye/') + 'public_key.pub').read()
        )
    sample_client = Client(
        '127.0.0.1',
        port=22,
        username='sheshtawy',
        password='a happy secret',
        mail='hisham.elsheshtawy@gmail.com',
        alerts=[cpu_alert, memory_alert]
    )

    yield sample_client
    sample_client.disconnect()
