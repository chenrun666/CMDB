"""
用户自定义配置
"""
import os
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


USER = "root"
EMAIL = "chenrun@163.com"

MODE = "AGENT"
DEBUG = True

API = "http://127.0.0.1:8000/api/asset/"

CERT_PATH = os.path.join(BASEDIR, "config/cert")

# 类似与django的中间件
PLUGINS_DICT = {
    'basic': "src.plugins.basic.Basic",
    'board': "src.plugins.board.Board",
    'cpu': "src.plugins.cpu.Cpu",
    'disk': "src.plugins.disk.Disk",
    'memory': "src.plugins.memory.Memory",
    'nic': "src.plugins.nic.Nic",
}
