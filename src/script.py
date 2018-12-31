from . import client
from lib.conf.config import settings


def run():
    if settings.MODE == "AGENT":
        obj = client.Agent()
    else:
        obj = client.SSHSALT()

    obj.execute()
