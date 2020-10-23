from api import log
from config import HOST


class ApiRegisterLogin:
    """登录注册资源接口封装"""

    # 初始化
    def __init__(self, session):
        self.session = session
        log.info("正在初始化 session对象：{}".format(self.session))
        """初始化以下5个接口的请求url"""
        # 图片验证码url
        self.__url_img_code = HOST + "/common/public/verifycode1/{}"
        # 注册手机验证码 url
        self.__url_phone = HOST + "/member/public/sendSms"
        # 注册url
        self.__url_register = HOST + "/member/public/reg"
        # 登录 url
        self.__url_login = HOST + "/member/public/login"
        # 查询 url
        self.__url_islogin = HOST + "/member/public/islogin"

    # 1. 注册图片验证码 接口封装
    def api_register_img_code(self, random):
        log.info("正在调用注册图片验证码接口 url：{}".format(self.__url_img_code.format(random)))
        # 请求
        return self.session.get(url=self.__url_img_code.format(random))

    # 2. 注册手机验证码 接口封装
    def api_phone_code(self, phone, imgVerifyCode):
        # 1. 定义参数
        data = {
            "phone": phone,
            "imgVerifyCode": imgVerifyCode,
            "type": "reg"
        }
        log.info("正在调用注册手机验证码接口 url：{} 请求参数数据：{}".format(self.__url_phone,data))

        # 2. 调用post方法 参数为data时，默认请求头为 form-data
        return self.session.post(url=self.__url_phone, data=data)

    # 3. 注册 接口封装
    def api_register(self, phone, password, verifycode, phone_code, dy_server, invite_phone):
        # 1. 定义参数
        data = {
            "phone": phone,
            "password": password,
            "verifycode": verifycode,
            "phone_code": phone_code,
            "dy_server": dy_server,
            "invite_phone": invite_phone,
        }
        log.info("正在调用注册接口 url：{} 请求参数数据：{}".format(self.__url_phone,data))

        # 2. 调用post方法 参数为data时，默认请求头为 form-data
        return self.session.post(url=self.__url_register, data=data)

    # 4. 登录接口封装
    def api_login(self,keywords,password):
        # 1. 定义参数
        data = {
            "keywords": keywords,
            "password": password
        }
        log.info("正在调用登录接口 url：{} 请求参数数据：{}".format(self.__url_phone,data))
        # 2. 调用post方法 参数为data时，默认请求头为 form-data
        return self.session.post(url=self.__url_login, data=data)

    # 5. 查询登录状态 接口封装
    def api_is_login(self):
        log.info("正在调用查询登录状态接口 url：{}".format(self.__url_phone))
        return self.session.post(url=self.__url_islogin)
