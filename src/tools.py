# -*- encoding: utf-8 -*-
"""
@File    :   tools.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/1 17:15   JeasonZhang      1.0         None
"""
from __future__ import annotations

import re
# import requests
# from selenium import webdriver
#
import time


def format_date(date_text: str) -> str | None:
    formatted_date: str | None = None
    # 匹配（August 4, 2023）格式的日期
    pattern1 = r"^(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}$"
    # 匹配（Aug 4, 2023）格式的日期
    pattern2 = r"^(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4}$"

    if re.match(pattern1, date_text):
        formatted_date = time.strftime("%Y-%m-%d", time.strptime(date_text, "%B %d, %Y"))
    if re.match(pattern2, date_text):
        formatted_date = time.strftime("%Y-%m-%d", time.strptime(date_text, "%b %d, %Y"))

    if formatted_date:
        return formatted_date
    else:
        return None
# webapi = webdriver.Chrome()
# webapi.implicitly_wait(10)  # 全局等待10s
# webapi.get('https://book.douban.com/')  # 通过selenium登录豆瓣读书首页
# sel_cookies = webapi.get_cookies()  # 获取selenium侧的cookies
#
# jar = requests.cookies.RequestsCookieJar()  # 先构建RequestsCookieJar对象
# for i in sel_cookies:
#     # 将selenium侧获取的完整cookies的每一个cookie名称和值传入RequestsCookieJar对象
#     # domain和path为可选参数，主要是当出现同名不同作用域的cookie时，为了防止后面同名的cookie将前者覆盖而添加的
#     jar.set(i['name'], i['value'], domain=i['domain'], path=i['path'])
#
# session = requests.session()  # requests以session会话形式访问网站
# session.cookies.update(jar)  # 将配置好的RequestsCookieJar对象加入到requests形式的session会话中
#
# url = 'https://book.douban.com/subject/4913064/'
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
# req = requests.Request(method='GET', url=url, headers=headers)
# rpe = session.send(session.prepare_request(req),
#                    verify=False,  # verify设置为False来规避SSL证书验证
#                    timeout=10)
#
# import requests
# from selenium import webdriver
#
# session = requests.session()  # requests以session会话形式访问网站
# url = 'https://book.douban.com/subject/4913064/'
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
# req = requests.Request(method='GET', url=url, headers=headers)
# rpe = session.send(session.prepare_request(req),
#                    verify=False,  # verify设置为False来规避SSL证书验证
#                    timeout=10)
#
# webapi = webdriver.Chrome()
# webapi.implicitly_wait(10)  # 全局等待10s
# webapi.get(url)
# webapi.get_cookies()  # 此时的selenium侧的cookies
# webapi.delete_all_cookies()  # 删除selenium侧的所有cookies
# for k, v in session.cookies.items():  # 获取requests侧的cookies
#     webapi.add_cookie({'name': k, 'value': v})  # 向selenium侧传入以requests侧cookies的name为键value为值的字典
# webapi.get_cookies()  # 此时的cookies同步为requests侧的cookies
