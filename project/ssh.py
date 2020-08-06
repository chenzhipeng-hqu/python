# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/05/30
# @Author  : 陈志鹏
# @File    : xx.py
"""

"""

__author__ = '陈志鹏'

import os
import sys
work_path = os.path.join(os.path.dirname(sys.argv[0]), "../")
sys.path.append(os.path.abspath(work_path))
os.chdir(work_path)

import paramiko
from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()


class SecureShell(object):

    def __init__(self, user, password, port, ips):
        self.user = user
        self.password = password
        self.port = port
        self.ip = ips

    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.ip, self.port, self.user, self.password)
            logger.info("连接已建立")
            return 0
        except Exception as e:
            logger.warn("未能连接到主机")
            return 1

    def cmd(self, cmd):
        # cmd = input("请输入要执行的命令:>>")
        self.ssh.exec_command(cmd)
        #logger.info(sys.stdout.read())

    def input(self):
        # self.local_file_abs = input("本地文件的绝对路径:>>")#'123456.txt' #
        # self.remote_file_abs = input("远程文件的绝对路径:>>")#'/home/root/123456.txt' #
        pass

    def put(self, local_file_abs, remote_file_abs):
        sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        sftp = self.ssh.open_sftp()
        # self.input()
        sftp.put(local_file_abs, remote_file_abs)

    def get(self, local_file_abs, remote_file_abs):
        sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        sftp = self.ssh.open_sftp()
        self.input()
        sftp.get(remote_file_abs, local_file_abs)

    def close(self):
        self.ssh.close()
        logger.info("连接关闭")

if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')
