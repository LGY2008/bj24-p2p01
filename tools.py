import json
import logging.handlers
import os
from config import BASE_DIR
from bs4 import BeautifulSoup
import pymysql

print("Base_dir1 :", BASE_DIR)


# 日志工具封装
class GetLog:
    logger = None

    @classmethod
    def get_log(cls):
        if cls.logger is None:
            # 1. 获取日志器
            cls.logger = logging.getLogger()
            # 2. 设置日志级别入口
            cls.logger.setLevel(logging.INFO)
            filepath = BASE_DIR + os.sep + "log" + os.sep + "p2p.log"
            # 3. 获取控制台处理或文件处理器
            th = logging.handlers.TimedRotatingFileHandler(filename=filepath,
                                                           when="midnight",
                                                           interval=1,
                                                           backupCount=3,
                                                           encoding="utf-8")
            # 4. 获取格式器
            fm = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s"
            fmt = logging.Formatter(fm)
            # 5. 将格式器添加到处理器中
            th.setFormatter(fmt)
            # 6. 将处理器添加到日志器
            cls.logger.addHandler(th)
        # 返回日志器
        return cls.logger


# 连接数据库类
class DBUtilMysql:
    # 1. 获取连接对象
    @classmethod
    def __get_conn(cls):
        return pymysql.connect(host="52.83.144.39", user="root", password="Itcast_p2p_20191228", database="czbk_member",
                               port=3306, charset="utf8")

    # 2. 执行sql方法
    @classmethod
    def execute_sql(cls, sql):
        # 1、获取连接对象
        conn = DBUtilMysql.__get_conn()
        # 2、获取游标对象
        cursor = conn.cursor()
        try:
            # 3、执行sql语句
            cursor.execute(sql)
            if sql.lower().split()[0] == "select":
                return cursor.fetchall()
            else:
                # 提交事务
                conn.commit()
                # 返回受影响的 行数
                return cursor.rowcount
        except:
            # 回滚事务
            conn.rollback()
            # 抛异常
            raise
        finally:
            # 关闭对象
            DBUtilMysql.__close(conn, cursor)

    # 3. 关闭对象操作
    @classmethod
    def __close(cls, conn=None, cursor=None):
        # 1. 先关闭游标
        if cursor:
            cursor.close()
        # 2. 关闭连接
        if conn:
            conn.close()


# 清空测试数据
def clear_test_data():
    # 1、清除用户信息表
    sql = """delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id where m.phone in ("13600001111","13600001112","13600001113","13600001114","13600001115");"""
    DBUtilMysql.execute_sql(sql)
    # 2、清除用户登录日志表
    sql = """delete l.* from mb_member_login_log l INNER JOIN mb_member m on l.member_id = m.id where m.phone in ("13600001111","13600001112","13600001113","13600001114","13600001115");"""
    DBUtilMysql.execute_sql(sql)
    # 3、清除用户主表数据
    sql = """delete from mb_member where phone in ("13600001111","13600001112","13600001113","13600001114","13600001115");"""
    DBUtilMysql.execute_sql(sql)
    # 4、清除用户注册日志表
    sql = """delete from mb_member_register_log where phone in ("13600001111","13600001112","13600001113","13600001114","13600001115");"""
    DBUtilMysql.execute_sql(sql)


# 断言封装
def common_assert(self, r, response_code=200, status_code=200, description=None):
    """
    :param self: TestCase实力对象
    :param r: 响应对象
    :param response_code: 响应状态吗
    :param status_code: 响应数据中status，如果不为空 就执行
    :param description: 响应数据中说明，如果不为空 就执行
    """
    try:
        # 断言响应状态吗
        self.assertEqual(response_code, r.status_code)
        if status_code:  # 不为None执行
            # 断言 响应数据 status
            self.assertEqual(status_code, r.json().get("status"))
        if description:
            # 断言 响应数据 description
            self.assertEqual(description, r.json().get("description"))
    except Exception as e:
        GetLog.get_log().error(e)
        # 抛异常
        raise


# 读取json文件工具
def read_json(filename, data_type):
    GetLog.get_log().info("正在调用 读取json工具...")
    filepath = BASE_DIR + os.sep + "data" + os.sep + filename
    arrs = []
    with open(filepath, "r", encoding="utf-8")as f:
        for data in json.load(f).get(data_type):
            # 1:为 切片 取出desc说明文字
            arrs.append(tuple(data.values())[1:])
    GetLog.get_log().info("==》调用读取json工具结果为：《=={}".format(arrs))
    return arrs


# 解析html方法
def html_parser(response):
    # 1、解析响应数据 并 获取html
    html = response.json().get("description").get("form")
    print("html:", html)
    soup = BeautifulSoup(html, "html.parser")
    # 2、提取 url
    url = soup.form.get("action")
    GetLog.get_log().info("提取的url为：{}".format(url))
    print("提取的url:", url)
    # 定义data 字典
    data = {}
    # 3、提取所有input标签 中name和value
    for input in soup.find_all("input"):
        data[input.get("name")] = input.get("value")
    return url, data


if __name__ == '__main__':
    sql = "select * from mb_member_register_log where phone in ('13600001111','13600001112');"
    print(DBUtilMysql.execute_sql(sql))
    # clear_test_data()
