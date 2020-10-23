# 1、导包
from bs4 import BeautifulSoup

html_file = """
<html> 
    <head>
    <title>黑马程序员</title>
    </head> 
    <body>
        <p id="test01">软件测试</p>
        <p id="test02">2020年</p>
        <a href="/api.html">接口测试</a>
        <a href="/web.html">Web自动化测试</a> 
        <a href="/app.html">APP自动化测试</a>
    </body>
</html>
"""

# 2、解析获取soup对象
soup = BeautifulSoup(html_file, "html.parser")

# 3、提取数据
# 提取
print(soup.title)  # 提取整个标签
print(soup.title.name)  # 提取标签名称
print(soup.title.string) # 提取标签字符串
print(soup.p.get("id"))  # 提取属性 或 soup.p['id']
print(soup.find_all("a")) # 查找一组标签方法 返回格式list