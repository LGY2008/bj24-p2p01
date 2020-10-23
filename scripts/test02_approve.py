import unittest

import requests
from parameterized import parameterized

from api import log
from api.api_common import ApiCommon
from tools import common_assert, read_json


class TestApprove(unittest.TestCase):
    # 初始化
    def setUp(self) -> None:
        # 获取session对象
        self.session = requests.session()
        # 获取ApiCommon对象
        self.common = ApiCommon(self.session)
        # 获取ApiApprove对象
        self.approve = self.common.get_api_approve()

    # 结束
    def tearDown(self) -> None:
        # 关闭session
        self.session.close()

    # 1、认证接口 测试方法
    @parameterized.expand(read_json("approve.json", "approve"))
    def test01_approve(self, realname, card_id, response_code, status_code,expect_msg):
        # 调用登录
        self.common.get_api_reg_login().api_login("13600001111", "test12345")
        # 调用 认证接口
        r = self.approve.api_approve(realname, card_id)
        log.info("认证结果为：{}".format(r.json()))
        print("认证结果为：", r.json())
        # 断言
        common_assert(self, r, response_code, status_code, expect_msg)

    # 2、认证查询接口 测试方法
    @parameterized.expand(read_json("approve.json", "get_approve"))
    def test02_get_approve(self, login_name, response_code, phone_4):
        # 调用登录
        self.common.get_api_reg_login().api_login(login_name, "test12345")
        # 调用查询认证接口
        r = self.approve.api_get_approve()
        log.info("认证查询结果为：{}".format(r.json()))
        # 断言
        common_assert(self, r,response_code=response_code, status_code=None)
        self.assertEqual(response_code, r.status_code)
        if phone_4:
            # 扩展 断言手机号 尾号
            phone = r.json().get("phone")
            print("phone:", phone)
            self.assertIn(phone_4, phone)
