# coding:utf-8
# 1、 导包
import unittest
import os, sys

sys.path.append(os.getcwd())
from HTMLTestRunner_HeiMa import HTMLTestRunner

# 2、定义测试套件
suite = unittest.defaultTestLoader.discover("./scripts")
# 3、实例化HTMLTestRunner类并调用run方法
with open("./report/report.html", "wb")as f:
    HTMLTestRunner(stream=f).run(suite)
