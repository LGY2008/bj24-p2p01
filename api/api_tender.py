from config import HOST


class ApiTender:
    """投资模块"""

    # 初始化方法
    def __init__(self, session):
        """初始化session对象及2个接口url"""
        # 1. 获取session对象
        self.session = session
        # 2. 定义投资接口 url
        self.__url_tender = HOST + "/trust/trust/tender"
        # 3. 定义投资列表接口 url
        self.__url_tender_list = HOST + "/loan/tender/mytenderlist"

    # 投资接口封装
    def api_tender(self, id, amount):
        # 1. 定义请求参数
        data = {
            "id": id,
            "depositCertificate": "-1",
            "amount": amount
        }
        # 2. 调用post方法
        return self.session.post(self.__url_tender, data=data)

    # 投资列表接口封装
    def api_tender_list(self):
        # 1. 定义请求参数
        data = {
            "status": "tender"
        }
        # 2. 调用post方法
        return self.session.post(self.__url_tender_list, data=data)
