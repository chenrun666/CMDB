import json

import requests

from src.plugins import PluginManager
from lib.conf.config import settings


class Base(object):
    def post_asset(self, server_info):
        requests.post(settings.API, json=server_info)


class Agent(Base):

    def execute(self):
        server_info = PluginManager().exec_plugin()
        self.post_asset(server_info)


class SSHSALT(Base):
    def get_host(self):
        # 获取未采集的主机列表
        response = requests.get(settings.API)
        result = json.loads(response.text)
        if not result["status"]:
            return
        return result["data"]

    def execute(self):
        host_list = self.get_host()
        for host in host_list:
            server_info = PluginManager(host).exec_plugin()
            self.post_asset(server_info)
