
# -*- coding: utf-8 -*-
# @File : dbopertor.py
# @Author: 叶永彬
# @Date : 2018/10/12
# @Desc : 数据库操作
import pymysql.cursors
import pymysql
import traceback
from Config.Config import Config
from common.logger import logger as log

class Db:
    def __init__(self, charset="utf-8"):
        self.host = Config().db
        self.user = Config().db_user
        self.password = Config().db_pwd
        self.port = int(Config().db_port)
        self.database = Config().db_name
        self.charset = charset

    # 数据库连接方法:
    def open(self):
        self.db = pymysql.connect(host=self.host, user=self.user,
                                  password=self.password, port=self.port,
                                  database=self.database,charset="utf8")
        # 游标对象
        self.cur = self.db.cursor()

    # 数据库关闭方法:
    def close(self):
        self.cur.close()
        self.db.close()

    # 数据库执行操作方法:
    def execute(self, sql, L=[]):
        self.open()
        try:
            self.open()
            self.cur.execute(sql, L)
            self.db.commit()
            print("ok")
        except Exception as e:
            self.db.rollback()
            print("Failed", e)
        self.close()

    # 数据库查询所有操作方法:
    def select(self, sql, L=[]):
        self.open()
        try:
            self.open()
            self.cur.execute(sql, L)
            result = self.cur.fetchall()
            print(type(result))
            if not result:
                result = (("null",),)
            return result[-1][0]
        except Exception as e:
            print("Failed", e)
        self.close()

if __name__ == "__main__":
    a =Db()
    csql = "select real_price from park_trader_coupon_template where NAME='api优惠劵4350'"
    result = str(a.select(csql))
    print(result)