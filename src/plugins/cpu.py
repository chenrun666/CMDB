"""
CPU信息
"""
import os
from lib.conf.config import settings


class Cpu(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def process(self, command_func, debug):
        if debug:
            output = open(os.path.join(settings.BASEDIR, "files/cpuinfo.out"), "r", encoding="utf-8").read()
        else:
            output = command_func("cat /proc/cpuinfo")
        return self.parse(output)

    def parse(self, content):
        """
        解析shell返回的命令
        :param content:
        :return:
        """
        response = {"cpu_count": 0, "cpu_physical_count": 0, "cpu_model": ""}

        cpu_physical_set = set()

        content = content.strip()
        for item in content.split("\n\n"):
            for row_line in item.split("\n"):
                key, value = row_line.split(":")
                key = key.strip()
                if key == "processor":
                    response['cpu_count'] += 1
                elif key == "physical id":
                    cpu_physical_set.add(value)
                elif key == "model name":
                    if not response['cpu_model']:
                        response["cpu_model"] = value

        response['cpu_physical_count'] = len(cpu_physical_set)

        return response
