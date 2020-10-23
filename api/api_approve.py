from config import HOST


class ApiApprove:
    """认证模块"""

    # 初始化
    def __init__(self, session):
        """定义 session和url"""
        self.session = session
        # 1. 定义认证url
        self.__url_approve = HOST + "/member/realname/approverealname"
        # 2. 定义查询认证url
        self.__url_get_approve = HOST + "/member/member/getapprove"

    # 1、认证接口 封装
    def api_approve(self, realname, card_id):
        """
            注意：认证请求参数格式为multipart/form-data
            实现：需要使用多中类型请求参数 files={"x":"y"}
        """
        # 1、定义请求参数
        data = {
            "realname": realname,
            "card_id": card_id
        }
        # 2、调用post方法 files={"x":"y"}为了满足多消息参数而临时引用。值随便写
        return self.session.post(self.__url_approve, data=data, files={"x": "y"})

    # 2、查询认证 接口封装
    def api_get_approve(self):
        return self.session.post(self.__url_get_approve)

