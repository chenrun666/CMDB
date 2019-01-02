import importlib
import traceback
from lib.conf.config import settings


class PluginManager(object):
    def __init__(self, hostname=None):
        self.hostname = hostname
        self.plugin_dict = settings.PLUGINS_DICT

        self.mode = settings.MODE
        self.debug = settings.DEBUG
        if self.mode == "SSH":
            self.ssh_user = settings.SSH_USER
            self.ssh_port = settings.SSH_PORT
            self.ssh_pwd = settings.SSH_PWD
            self.ssh_key = settings.SSH_KEY

    def exec_plugin(self):
        """
        获取所有的插件，并执行获取插件的返回值
        :return:
        """
        response = {}
        for k, v in self.plugin_dict.items():
            # 'basic': "src.plugins.basic.Basic"
            ret = {"status": True, "data": None}
            try:
                prefix, class_module = v.rsplit(".", 1)
                m = importlib.import_module(prefix)
                cls = getattr(m, class_module)
                if hasattr(cls, "initial"):
                    obj = cls.initial()
                else:
                    obj = cls()
                result = obj.process(self.command, self.debug)
                ret["data"] = result
            except Exception:
                ret["status"] = False
                ret["data"] = f"[{self.hostname if self.hostname else 'AGENT'}][{prefix}]采集信息出现错误：" \
                              f"{traceback.format_exc()}"

            response[k] = ret

        return response

    def command(self, cmd):
        if self.mode == "AGENT":
            return self.__agent(cmd)
        elif self.mode == "SSH":
            return self.__ssh(cmd)
        elif self.mode == "SALT":
            return self.__salt(cmd)
        else:
            raise Exception("请选择AGENT/SSH/SALT模式")

    def __agent(self, cmd):
        import subprocess
        output = subprocess.getoutput(cmd)
        return output

    def __salt(self, cmd):
        salt_cmd = f"salt {self.hostname} cmd.run '{cmd}'"
        import subprocess
        output = subprocess.getoutput(salt_cmd)
        return output

    def __ssh(self, cmd):
        import paramiko

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result
