from forteauto import __version__
from fastapi import status

def test_version():
    assert __version__ == '0.1.0'



def test_root(client):
    with client as client:
            res = client.get("/")
    assert res.status_code == status.HTTP_200_OK