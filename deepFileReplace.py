#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 16:09
# @Author  : 叶永彬
# @File    : deepFileReplace.py

import os

class DeepFileReplace():
    """文件递归替换内容"""
    def __init__(self):
        self.filePathLsit = []

    def alter(self,file, old_str, new_str):
        """替换文件中的字符串"""
        file_data = ''
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                if old_str in line:
                    line = line.replace(old_str, new_str)
                file_data += line
        with open(file, "w", encoding="utf-8") as f:
            f.write(file_data)

    def getFilePath(self,folder):
        """递归文件夹"""
        if os.path.isdir(folder):
            fileList = os.listdir(folder)
            for k in fileList:
                path = os.path.join(folder, k)
                if os.path.isfile(path):
                    self.filePathLsit.append(path)
                else:
                    filePath = path + '/'
                    self.getFilePath(filePath)
        return self.filePathLsit

    def testRun(self,folder,str,newStr):
        filePathList = self.getFilePath(folder)
        for i in filePathList:
            self.alter(i,str,newStr)
        print("执行完成...")

if __name__ == '__main__':
    floder = "E:/KPoco/test_data/"
    DeepFileReplace().testRun(floder,'test','test111')