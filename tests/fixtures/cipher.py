import pytest
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from hawkeye import settings

@pytest.fixture
def cipher():
    private_key = RSA.importKey(open(settings.PRIVATE_KEY_PATH).read())
    return PKCS1_OAEP.new(private_key)
