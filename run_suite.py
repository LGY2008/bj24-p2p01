# 1、 导包
import unittest
from lib.HTMLTestRunner import HTMLTestRunner
# 2、定义测试套件
suite = unittest.defaultTestLoader.discover("./scripts")
# 3、实例化HTMLTestRunner类并调用run方法
with open("./report/report.html", "wb")as f:
    HTMLTestRunner(stream=f).run(suite)
