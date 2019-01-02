"""
硬盘信息
"""
import re
import os
from lib.conf.config import settings


class Disk(object):

    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def process(self, command_func, debug):
        if debug:
            output = open(os.path.join(settings.BASEDIR, "files/disk.out"), "r", encoding="utf-8").read()
        else:
            output = command_func("sudo MegaCli  -PDList -aALL")
        return self.parse(output)

    def parse(self, content):
        response = {}
        result = []
        for row_line in content.split("\n\n\n\n"):
            result.append(row_line)
        for item in result:
            temp_dict = {}
            for row in item.split('\n'):
                if not row.strip():
                    continue
                if len(row.split(':')) != 2:
                    continue
                key, value = row.split(':')
                name = self.mega_patter_match(key)
                if name:
                    if key == 'Raw Size':
                        raw_size = re.search('(\d+\.\d+)', value.strip())
                        if raw_size:

                            temp_dict[name] = raw_size.group()
                        else:
                            raw_size = '0'
                    else:
                        temp_dict[name] = value.strip()
            if temp_dict:
                response[temp_dict['slot']] = temp_dict
        return response

    @staticmethod
    def mega_patter_match(needle):
        grep_pattern = {'Slot': 'slot', 'Raw Size': 'capacity', 'Inquiry': 'model', 'PD Type': 'pd_type'}
        for key, value in grep_pattern.items():
            if needle.startswith(key):
                return value
        return False



if __name__ == '__main__':
    output = open("../../files/disk.out").read()
    content = output.strip().split("\n\n\n")
    # print(content[0].strip().split("\n"))

    disk_li = []
    for item in content:
        disk_li.append(item)
    for i in disk_li:
        temp_dic = {}
        for j in i.strip().split("\n"):
            info = j.strip().split(":")
            if len(info) < 2:
                continue
            else:
                key, value = info


