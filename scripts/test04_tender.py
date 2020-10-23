import unittest

import requests
from parameterized import parameterized

from api import log
from api.api_common import ApiCommon
from tools import html_parser, read_json, common_assert, clear_test_data


class TestTender(unittest.TestCase):

    # 初始化
    def setUp(self) -> None:
        # 获取session对象
        self.session = requests.session()
        # 获取ApiCommon对象
        self.common = ApiCommon(self.session)
        # 调用登录
        self.common.get_api_reg_login().api_login("13600001111", "test12345")
        # 获取投资对象
        self.tender = self.common.get_tender()

    # 结束
    def tearDown(self) -> None:
        print("=="*50)
        print("运行结束，测试数据清除完毕！")
        print("=="*50)
        # 关闭session
        self.session.close()

    @classmethod
    def tearDownClass(cls) -> None:
        # 清除测试数据
        clear_test_data()

    # 投资接口测试方法
    @parameterized.expand(read_json("tender.json", "tender"))
    def test01_tender(self, id, amount, expect_msg):
        TestTender.id_list = id
        # 调用投资接口
        r = self.tender.api_tender(id, amount)
        print(r.json())
        if amount == "":
            # 断言
            common_assert(self,r,status_code=100,description=expect_msg)
        else:
            # 提取html
            result = html_parser(r)
            # 调用三方投资
            r = self.session.post(result[0], result[1])
            log.info("三方投资结果为：{}".format(r.text))
            print("投资结果为：", r.text)
            # 断言
            self.assertEqual(expect_msg, r.text)

    # 投资列表接口测试方法
    @parameterized.expand(read_json("tender.json", "tender_list"))
    def test02_tender_list(self, expect_id):
        # 调用 我的投资列表接口
        r = self.tender.api_tender_list()
        print("投资列表结果为：{}".format(r.json()))
        log.info("投资列表结果为：{}".format(r.json()))
        print("我的投资列表产品ID为：", r.json().get("items")[0].get("loan_id"))
        # 断言
        self.assertEqual(expect_id, r.json().get("items")[0].get("loan_id"))

    # 投资业务接口测试方法
    @parameterized.expand(read_json("tender.json", "tender_reg_tender"))
    def test03_reg_tender(self, random, phone, img_code, phone_code, password, dy_server, invite_phone, amount, id,
                          expect_msg):
        # 1、注册图片验证码接口
        self.common.get_api_reg_login().api_register_img_code(random)
        # 2、注册手机验证码
        self.common.get_api_reg_login().api_phone_code(phone, img_code)
        # 3、注册接口
        r = self.common.get_api_reg_login().api_register(phone=phone,
                                                         password=password,
                                                         verifycode=img_code,
                                                         phone_code=phone_code,
                                                         dy_server=dy_server,
                                                         invite_phone=invite_phone)
        print("注册结果为：{}".format(r.json()))
        # 4、登录接口
        r = self.common.get_api_reg_login().api_login(keywords=phone, password=password)
        print("登录结果为：{}".format(r.json()))
        # 5、开户请求
        r = self.common.get_api_trust().api_trust()
        # 6、三方开户
        result = html_parser(r)
        r = self.session.post(result[0], result[1])
        print("业务方法-三方开户结果为：{}".format(r.text))
        log.info("业务方法-三方开户结果为：{}".format(r.text))
        # 7、充值验证码
        self.common.get_api_trust().api_trust_code(random)
        # 8、充值接口
        r = self.common.get_api_trust().api_trust_recharge(amount=amount, valicode=img_code)
        # 9、三方充值
        result = html_parser(r)
        r = self.session.post(result[0], result[1])
        print("业务方法-三方充值结果为：{}".format(r.text))
        log.info("业务方法-三方充值结果为：{}".format(r.text))
        # 10、投资接口
        r = self.common.get_tender().api_tender(id, amount=amount)
        # 11、三方投资
        result = html_parser(r)
        r = self.session.post(result[0], result[1])
        print("业务方法-三方投资结果为：{}".format(r.text))
        log.info("业务方法-三方投资结果为：{}".format(r.text))
        try:
            self.assertEqual(expect_msg, r.text)
        except Exception as e:
            log.error(e)
            raise
