from config import HOST


class ApiTrust:
    """开户充值 接口封装"""

    # 初始化
    def __init__(self, session):
        """初始化session对象和以下3个接口url"""
        self.session = session
        # 1. 开户url
        self.__url_trust = HOST + "/trust/trust/register"
        # 2. 充值验证码url
        self.__url_trust_code = HOST + "/common/public/verifycode/{}"
        # 3. 充值url
        self.__url_trust_recharge = HOST + "/trust/trust/recharge"

    # 1、开户接口封装
    def api_trust(self):
        # 调用post方法
        return self.session.post(self.__url_trust)

    # 2、充值验证码接口封装
    def api_trust_code(self, random):
        # 调用get方法
        return self.session.get(self.__url_trust_code.format(random))

    # 3、充值接口封装
    def api_trust_recharge(self, amount, valicode):
        # 定义 参数数据
        data = {
            "paymentType": "chinapnrTrust",
            "amount": amount,
            "formStr": "reForm",
            "valicode": valicode
        }
        # 调用post方法
        return self.session.post(self.__url_trust_recharge, data=data)
