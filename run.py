# import subprocess
#
# import requests
#
# v = subprocess.getoutput("ifconfig")
#
# v2 = subprocess.getoutput("ls")
#
# url = "http://127.0.0.1:8000/asset"
#
# requests.post(url, data={"k1": "v1"})

# 弊端： 每一台机器都要有agent，耗费没台机器的性能
# 机器太多就用agent


##############################################################################
# 方式2 中控机放一份就可以了
# pip install paramiko

# 远程连接服务器，获取结果发送给API
"""
import paramiko
import requests

# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname="123.207.56.67", port=22, username='root', password="")

# 执行命令
stdin, stdout, stderr = ssh.exec_command("uname -a")  # 后续，结果，出错
# 获取命令结果
result = stdout.read()
print(result)

url = "http://127.0.0.1:8000/asset"
requests.post(url=url, data={"k": "v"})

# 关闭连接
ssh.close()

"""


# 缺点： ssh速度会满。
# SSH方法：
#   - fabric
#   - ansible

# 应用场景：
#  - 机器不多就用paramiko


##############################################################################
# 第三种方式：saltstack（python开发的）
# master  yum install salt-master
    # 配置： 1.1.1.1
    #  - service salt-master start
# salve   yum install salt-minion
    #  - master: 1.1.1.1
# salve   yum install salt-minion

# 授权
"""
salt-key -L
salt-key -A
salt-key '*' cmd.run 'hostname'
"""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="10.0.0.10", port=22, username="root", password="123")

stdin, stdout, stderr = ssh.exec_command("salt '*' cmd.run 'hostname'")

result = stdout.read()

print(result)


# import salt.client
# local = salt.client.LocalClient()
# result = local.cmd("xxx.com", "cmd.run", ["ifconfig"])
# result是个字典 {"hostname": "结果"}

# saltstack 原理： rpc
# 优点
# master中维护了一个消息队列。每个salve从master的消息队列中那命令。
# salve将结果从放到另一个队列，master从中拿到消息。

# 应用场景： 机器比较多，公司也用saltstack

##############################################################################

# 第四种方式（不推荐使用）
#   puppet（比较老）Ruby开发
# master和salve会默认30分钟访问一次

##############################################################################

# 目标：
"""
1， Agent
2， SSH类，paramiko
3， saltstack

兼容三种采集方式软件
"""