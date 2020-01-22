
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
    def select(self, sql, L=[],showAll = "0"):
        self.open()
        try:
            self.open()
            self.cur.execute(sql, L)
            result = self.cur.fetchall()
            if not result:
                result = (("null",),)
            if showAll == "0":
                return result[-1][0]
            else:
                return list(result[-1])

        except Exception as e:
            print("Failed", e)
        self.close()

if __name__ == "__main__":
    a =Db()
    csql = "select * from user_trader_coupon where CAR_CODE='粤Q12348'"
    result = a.select(csql,showAll="1")
    # print(result)
    json = {
        "id":result[0],
        "canCover":result[18],
        "cityType":result,
        "couponName":result[1],
        "couponType":result[4],
        "couponUseEnum":result,
        "extPro":"",
        "faceValue":result[5],
        "favorVal":result,
        "groupKey":result,
        "maxCoverNum":result[19],
        "serialNumber":result[2],
        "traderCouponTemplateId":result,
        "useRule":result[17],
        "validFrom":result[6],
        "validTo":result[7]
    }
    print(result)