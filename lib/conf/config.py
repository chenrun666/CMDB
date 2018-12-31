"""
全局配置文件
"""
import os
import importlib
from . import global_settings


class Settings(object):
    def __init__(self):
        # 找到默认配置
        for name in dir(global_settings):
            value = getattr(global_settings, name)
            setattr(self, name, value)

        # 找到自定义配置
        settings_module = os.environ.get("USER_SETTINGS")
        # 根据字符串导入模块
        if settings_module:
            m = importlib.import_module(settings_module)
            for name in dir(m):
                if name.isupper():
                    value = getattr(m, name)
                    setattr(self, name, value)


settings = Settings()
