from api.api_approve import ApiApprove
from api.api_register_login import ApiRegisterLogin
from api.api_tender import ApiTender
from api.api_trust import ApiTrust


class ApiCommon:
    """api模块对象统一管理"""
    def __init__(self, session):
        self.session = session

    # 获取 注册登录对象
    def get_api_reg_login(self):
        return ApiRegisterLogin(self.session)

    # 获取 认证对象
    def get_api_approve(self):
        return ApiApprove(self.session)

    # 获取 开户充值对象
    def get_api_trust(self):
        return ApiTrust(self.session)

    # 获取 投资对象
    def get_tender(self):
        return ApiTender(self.session)