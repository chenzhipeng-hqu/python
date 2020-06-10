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

from project import log

from email.mime.text import MIMEText
import poplib
import smtplib

logger = log.Log(__name__, log_path=os.getcwd()).getlog()

class EMailManager(object):
    '''

    '''
    def __init__(self):
        self.popHost = 'pop.qq.com'
        self.smtpHost = 'smtp.qq.com'
        self.port = 25
        self.userName = '874298842@qq.com'
        self.passWord = 'qpkjlskwxnnpbfaa'
        # self.bossMail = 'chenzhipeng3472@cvte.com'
        # self.bossMail = '874298842@qq.com'
        self.login()
        self.configMailBox()

    def login(self):
        try:
            self.mailLink = poplib.POP3_SSL(self.popHost)
            self.mailLink.set_debuglevel(0)
            self.mailLink.user(self.userName)
            self.mailLink.pass_(self.passWord)
            self.mailLink.list()
            logger.info (u'login success!')
        except Exception as e:
            logger.info (u'login fail! ' + str(e))
            quit()

    # 获取邮件
    def retrMail(self):
        try:
            mail_list = self.mailLink.list()[1]
            logger.info ("1")
            if len(mail_list) == 0:
                return None
            logger.info ("2")
            mail_info = str(mail_list[0]).split(' ')
            logger.info ("3")
            number = mail_info[0]
            logger.info ("4")
            logger.info(type(number))
            mail = self.mailLink.retr(number)[1]
            logger.info ("5")
            self.mailLink.dele(number)
            logger.info ("6")
            subject = u''
            sender = u''

            for i in range(0, len(mail)):
                if mail[i].startswith('Subject'):
                    subject = mail[i][9:]

                if mail[i].startswith('X-Sender'):
                    sender = mail[i][10:]

            content = {'subject': subject, 'sender': sender}

            return content

        except Exception as e:
            logger.info (str(e))
            return None

    def configMailBox(self):
        try:
            self.mail_box = smtplib.SMTP(self.smtpHost, self.port)
            self.mail_box.login(self.userName, self.passWord)
            logger.info (u'config mailbox success!')
        except Exception as e:
            logger.info (u'config mailbox fail! ' + str(e))
            quit()

    # 发送邮件
    def sendMsg(self, mail_body='Success!', toMail='chenzhipeng3472@cvte.com'):
        try:
            msg = MIMEText(mail_body, 'plain', 'utf-8')
            msg['Subject'] = mail_body
            msg['from'] = self.userName
            self.mail_box.sendmail(self.userName, toMail, msg.as_string())
            logger.info (u'send mail success!')
        except Exception as e:
            logger.info(u'send mail fail! ' + str(e))


if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')
    mailManager = EMailManager()

    # mail = mailManager.retrMail()

    # if mail != None:

    # logger.info (mail)

    mailManager.sendMsg(toMail='874298842@qq.com')
    # mailManager.sendMsg(toMail='chenzhipeng3472@cvte.com')



