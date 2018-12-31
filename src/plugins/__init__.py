import importlib
import traceback
from lib.conf.config import settings


class PluginManager(object):
    def __init__(self, hostname=None):
        self.hostname = hostname
        self.plugin_dict = settings.PLUGINS_DICT

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
                result = obj.process()
                ret["data"] = result
            except Exception:
                ret["status"] = False
                ret["data"] = f"[{self.hostname if self.hostname else 'AGENT'}][{prefix}]采集信息出现错误：" \
                              f"{traceback.format_exc()}"

            ret["data"] = ret

        return response
