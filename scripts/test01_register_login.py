import unittest
from time import sleep

import requests, random
from parameterized import parameterized
from api import log
from api.api_register_login import ApiRegisterLogin
from tools import common_assert, read_json, clear_test_data


# phone = "13600001111"
# pwd = "test123456"
# imgVerifyCode = "8888"
# phone_code = "666666"


class TestRegisterLogin(unittest.TestCase):
    """注册登录测试用例"""
    @classmethod
    def setUpClass(cls) -> None:
        # 清除测试数据
        clear_test_data()

    # 初始化
    def setUp(self) -> None:
        log.info("正在调用初始化方法")
        # 1. 获取session对象
        self.session = requests.session()
        log.info("正在获取session对象 {}".format(self.session))
        # 2. 获取ApiRegisterLogin对象
        self.reg_login = ApiRegisterLogin(self.session)
        log.info("正在获取ApiRegisterLogin对象 {}".format(self.reg_login))

    # 结束/销毁
    def tearDown(self) -> None:
        log.info("正在执行关闭session对象")
        # 关闭session对象
        self.session.close()

    # 1. 测试 注册图片验证码接口
    @parameterized.expand(read_json("reg_login.json", "img_code"))
    def test01_reg_img(self, random, response_code):
        r = self.reg_login.api_register_img_code(random)
        log.info("正在调用 注册图片验证码接口测试方法，响应状态码结果：{}".format(r.status_code))
        print("状态码：", r.status_code)
        print("结果为：", r.text)
        # 调用 公共断言
        common_assert(self, r, response_code=response_code, status_code=None)

    # 2. 测试 注册手机验证码接口
    @parameterized.expand(read_json("reg_login.json", "phone_code"))
    def test02_reg_phone(self, phone, imgVerifyCode, response_code, status_code, expect_msg):
        # 1、调用图片验证码
        self.reg_login.api_register_img_code(random.random())
        # 2、调用注册手机验证码接口
        r = self.reg_login.api_phone_code(phone=phone, imgVerifyCode=imgVerifyCode)
        # 3、断言
        print(r.status_code)
        log.info("正在调用 注册手机验证码接口测试方法，响应状态码结果：{}".format(r.json()))
        print("响应结果为：", r.json())
        common_assert(self, r=r, response_code=response_code, status_code=status_code, description=expect_msg)

    # 3. 测试 注册接口
    @parameterized.expand(read_json("reg_login.json", "register"))
    def test03_register(self, phone, password, verifycode, phone_code, dy_server, invite_phone, response_code,
                        status_code, expect_msg):
        sleep(1)
        # 1、调用图片验证码
        self.reg_login.api_register_img_code(random.random())
        # 2、调用注册手机验证码接口
        self.reg_login.api_phone_code(phone=phone, imgVerifyCode=verifycode)
        # 3、注册
        r = self.reg_login.api_register(phone, password, verifycode, phone_code, dy_server, invite_phone)
        log.info("注册接口请求的数据为：{}".format([phone, password, verifycode, phone_code, dy_server, invite_phone]))
        # 4、断言
        log.info("注册结果为：{}".format(r.text))
        common_assert(self, r, response_code, status_code, expect_msg)

    # 4. 测试 登录接口
    @parameterized.expand(read_json("reg_login.json", "login"))
    def test04_login(self, keywords, password, response_code, status_code, expect_msg):
        # 判断是否测试 密码错误次数
        if password == "error":
            pass
            # i = 1
            # # 循环错误3次调用
            # while i <= 3:
            #     r = self.reg_login.api_login(keywords, password)
            #     log.info("登录密码错误次数验证：第 {}次，响应状态码结果：{}".format(i, r.json()))
            #     print("登录结果为：", r.json())
            #     i += 1
            # # 暂停60秒 等待解锁
            # sleep(60)
            # # 验证码 登录是否成功
            # r = self.reg_login.api_login(keywords="13600001111", password="test12345")
            # print("解锁后登录结果为：", r.json())
            # log.info("锁定60秒解锁后，登录结果：{}".format(r.json()))
            # common_assert(self, r, response_code, status_code, expect_msg)
        else:
            # 非密码错误次数验证 调用
            r = self.reg_login.api_login(keywords, password)
            log.info("正在调用 登录接口测试方法，响应状态码结果：{}".format(r.json()))
            # 断言
            common_assert(self, r, response_code, status_code, expect_msg)

    # 5. 测试 是否登录接口
    @parameterized.expand(read_json("reg_login.json", "is_login"))
    def test05_is_login(self, is_login, response_code, status_code, expect_msg):
        if is_login == "已登录":
            # 1.调用登录
            self.reg_login.api_login(keywords="13600001111", password="test12345")
            # 调用查询登录接口
        r = self.reg_login.api_is_login()
        print("登录状态为：", r.json())
        log.info("正在调用 是否登录接口 测试方法，响应状态码结果：{}".format(r.json()))
        common_assert(self, r, response_code, status_code, expect_msg)
