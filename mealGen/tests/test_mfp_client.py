# testing the mfp client 
import pytest 
from core.util.mfp_client import MfpClient

def test_dowload_cookies():
    c = MfpClient()
    assert c.download_cookies() is True, "Failure: Cookie Download"

def test_set_cookies():
    c = MfpClient()
    c.download_cookies()
    assert client.set_cookies() is True, "Failure: Cookie Set"

def test_make_and_auth_device():
    c = MfpClient()
    c.download_cookies()
    c.set_cookies()
    device = client.make_and_auth_device()
    assert device is not None, "Failure: device authentication"

def test_get_data():
    client = MfpClient()
    client.download_cookies()
    client.make_and_auth_device()
    client.get_data("20204-01-01", "2024-01-31")
    assert client.data is not None, "Failure: data download"