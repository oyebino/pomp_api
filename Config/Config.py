# -*- coding: utf-8 -*- 
# @File : config.py
# @Author: 叶永彬
# @Date : 2018/9/13 
# @Desc : 读取config.ini 配置文件

from configparser import ConfigParser
import os
from sys import argv

class Config(object):

    VALUE_ENT_HOST = "host"
    VALUE_ENT_PARK_USER = "user"
    VALUE_ENT_PARK_PASSWORD = "password"
    VALUE_ENT_DB = "DB"
    VALUE_ENT_DB_PORT = "port"
    VALUE_ENT_DB_NAME = "db_name"
    VALUE_ENT_DB_USER = "db_user"
    VALUE_ENT_DB_PWD = "db_pwd"
    VALUE_ENT_ZBY_HOST = "ZBY_HOST"
    VALUE_ENT_MONITOR_HOST = "MONITOR_HOST"
    VALUE_ENT_ZBY_USER = "zby_user"
    VALUE_ENT_ZBY_PWD = "zby_pwd"
    VALUE_ENT_MONITOR_USER = "monitor_user"
    VALUE_ENT_MONITOR_PWD = "monitor_pwd"
    VALUE_ENT_AOMP_HOST = "AOMP_HOST"
    VALUE_ENT_AOMP_USER = "aomp_user"
    VALUE_ENT_AOMP_PWD = "aomp_pwd"
    VALUE_ENT_WEIXIN_HOST = "WEIXIN_HOST"
    VALUE_ENT_WEIXIN_USER = "weixin_user"
    VALUE_ENT_WEIXIN_PWD = "weixin_pwd"
    VALUE_ENT_OPENYDT_HOST = "openYDT_host"
    VALUE_ENT_MOCK_HOST = "mock_host"

    def __init__(self,env="SIT"):

        self.CATEGORY = env
        self.config = ConfigParser()

        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.ini')
        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")

        self.config.read(self.conf_path,encoding="UTF-8")
        self.host = self.config.get(self.CATEGORY,self.VALUE_ENT_HOST)
        self.db = self.config.get(self.CATEGORY,self.VALUE_ENT_DB)
        self.db_user = self.config.get(self.CATEGORY, self.VALUE_ENT_DB_USER)
        self.db_pwd = self.config.get(self.CATEGORY, self.VALUE_ENT_DB_PWD)
        self.db_port = self.config.get(self.CATEGORY,self.VALUE_ENT_DB_PORT)
        self.db_name = self.config.get(self.CATEGORY,self.VALUE_ENT_DB_NAME)
        self.user = self.config.get(self.CATEGORY, self.VALUE_ENT_PARK_USER)
        self.password = self.config.get(self.CATEGORY, self.VALUE_ENT_PARK_PASSWORD)
        self.monitor_host = self.config.get(self.CATEGORY,self.VALUE_ENT_MONITOR_HOST)
        self.monitor_user = self.config.get(self.CATEGORY,self.VALUE_ENT_MONITOR_USER)
        self.monitor_pwd = self.config.get(self.CATEGORY,self.VALUE_ENT_MONITOR_PWD)
        self.zby_host = self.config.get(self.CATEGORY,self.VALUE_ENT_ZBY_HOST)
        self.zby_user = self.config.get(self.CATEGORY,self.VALUE_ENT_ZBY_USER)
        self.zby_pwd = self.config.get(self.CATEGORY,self.VALUE_ENT_ZBY_PWD)
        self.aomp_host = self.config.get(self.CATEGORY, self.VALUE_ENT_AOMP_HOST)
        self.aomp_user = self.config.get(self.CATEGORY, self.VALUE_ENT_AOMP_USER)
        self.aomp_pwd = self.config.get(self.CATEGORY, self.VALUE_ENT_AOMP_PWD)
        self.weiXin_host = self.config.get(self.CATEGORY, self.VALUE_ENT_WEIXIN_HOST)
        self.weiXin_user = self.config.get(self.CATEGORY, self.VALUE_ENT_WEIXIN_USER)
        self.weiXin_pwd = self.config.get(self.CATEGORY, self.VALUE_ENT_WEIXIN_PWD)
        self.openYDT_host = self.config.get(self.CATEGORY, self.VALUE_ENT_OPENYDT_HOST)
        self.mock_host = self.config.get(self.CATEGORY, self.VALUE_ENT_MOCK_HOST)


    def get(self, title, value):
        return self.config.get(title, value)

    def getValue(self, value, title="SIT"):
        return self.config.get(title,value)

if __name__=='__main__':
    C = Config().mock_host
    print(C)
    # print(C.getValue("weiXin_host"))
