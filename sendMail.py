#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/26 16:21
# @Author  : yyb
# @File    : sendMail.py

import yagmail
import time
import os



class Mail():
    def __init__(self):
        self.yag = yagmail.SMTP(user="10219@akeparking.cn", password="Ake01997", host="hwsmtp.exmail.qq.com")
        self.tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.subject = "自动化报告_"+self.tm

        self.htmlBody= "test123"

        self.contents = [self.htmlBody, os.path.join(os.path.dirname(__file__), 'web-report.bat')]

    def send(self,receiver):
        self.yag.send(to=receiver,subject = self.subject,contents = self.contents)

from twilio.rest import Client

class Phone():
    def sendPhoneMessage(self,toPhone):
        sid = 'ACedd13f6bde6bdc9fb3797888dce29572'
        token = 'cda1b783bbb549e46126a2572cd5a01f'
        client = Client(sid,token)
        client.messages.create(body='this is my twilio message,test123',from_='+12055284403',to=toPhone)


if __name__=="__main__":

    # Mail().send('10219@akeparking.cn')
    Phone().sendPhoneMessage('+8613531412589')