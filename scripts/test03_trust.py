import unittest

import requests
from parameterized import parameterized

from api import log
from api.api_common import ApiCommon
from tools import html_parser, common_assert, read_json


class TestTrust(unittest.TestCase):
    # 初始化
    def setUp(self) -> None:
        # 获取session对象
        self.session = requests.session()
        # 获取ApiCommon对象
        self.common = ApiCommon(self.session)
        # 调用登录接口
        self.common.get_api_reg_login().api_login("13600001111", "test12345")
        # 获取ApiTrust对象
        self.trust = self.common.get_api_trust()

    # 结束
    def tearDown(self) -> None:
        # 关闭session
        self.session.close()

    # 开户接口测试方法
    @parameterized.expand(read_json("trust.json", "trust"))
    def test01_trust(self, expect_msg):
        log.info("开户参数化 expect_msc的值为：{}".format(expect_msg))
        # 1、调用开户接口
        r = self.trust.api_trust()
        log.info("开户结果：{}".format(r.json()))
        # 2、提取html数据
        result = html_parser(r)
        log.info("提取开户三方请求数据结果：{}".format(result))
        # 3、请求三方开户
        r = self.session.post(result[0], data=result[1])
        log.info("三方开户请求结果：{}".format(r.text))
        # 4. 断言
        self.assertEqual(expect_msg, r.text)

    # 充值验证码接口测试方法
    @parameterized.expand(read_json("trust.json", "trust_code"))
    def test02_trust_code(self, random, response_code):
        r = self.trust.api_trust_code(random)
        print("r:", r.text)
        log.info("充值验证码返回响应状态码为：{}".format(r.status_code))
        common_assert(self, r, response_code=response_code, status_code=None)

    # 充值接口测试方法
    @parameterized.expand(read_json("trust.json", "trust_recharge"))
    def test03_trust_recharge(self, amount, valicode, expect_msg):
        # 充值验证码
        self.trust.api_trust_code(12312313)
        # 1. 调用充值接口
        r = self.trust.api_trust_recharge(amount, valicode)
        log.info("充值接口返回结果：{}".format(r.json()))
        if valicode != 8888:
            common_assert(self, r, status_code=100, description=expect_msg)
        else:
            # 2. 提取html
            result = html_parser(r)
            log.info("提取充值三方请求数据结果：{}".format(result))
            # 3. 调用三方充值
            r = self.session.post(result[0], data=result[1])
            log.info("三方充值结果：{}".format(r.text))
            # 4. 断言
            print(r.text)
            self.assertEqual(expect_msg, r.text)
