import time
from getMainPage import Common
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import json
import requests
import jsonpath
from lxml import etree


class Entry(object):
    def __init__(self, p_time, p_name, p_position, p_content, p_with_link, p_address, p_link_content):
        self.time = p_time
        self.name = p_name
        self.position = p_position
        self.content = p_content
        self.with_link = p_with_link
        self.address = p_address
        self.link_content = p_link_content

    def __str__(self):
        print(f'{self.time}, {self.name}, '
              f'{self.position}, {self.content}, '
              f'{self.with_link}, {self.address}, '
              f'{self.link_content}')


class DataModel(object):
    def __init__(self):
        self.entries = []

    def append(self, p_entry):
        self.entries.append(p_entry)


# 判断文件是否自身执行，如果是则，执行之后的语句
if __name__ == '__main__':
    # com = Common()
    file = open("content.txt", "w+", encoding="utf8")
    for url in open("url_json.txt", "r", encoding="utf8"):
        print(url)
        url = url.replace('\n', '')
        try:
            # com.open_url(url)
            # cookies = com.browser.get_cookies()
            # print(cookies)
            # proxies = {
            #     "http": "http://127.0.0.1:7890",
            #     "https": "http://127.0.0.1:7890",
            # }

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7",
                "Sec-Ch-Ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "\"Windows\"",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/105.0.0.0 Safari/537.36",
            }
            # response = requests.get(url)  # , headers=headers, proxies=proxies, verify=False)
            # print(response.status_code)
            # # if response.status_code == 400:
            # url2 = response.links.get('alternate')['url']
            # print(url2)
            response1 = requests.get(url, headers=headers)  # , proxies=proxies, verify=False)
            # if response1.status_code == 200:
            json_dict = response1.content.decode()
            print(json_dict)
            jsonobj = json.loads(json_dict)

            article_id = jsonpath.jsonpath(jsonobj, 'id')
            article_content = jsonpath.jsonpath(jsonobj, 'content.rendered')
            article_slug = jsonpath.jsonpath(jsonobj, 'slug')
            article_url = jsonpath.jsonpath(jsonobj, 'guid.rendered')
            article_author = jsonpath.jsonpath(jsonobj, 'author')

            # entry = Entry()
            line = str(article_id)[2:-2] + '\t' + str(article_author)[2:-2] + '\t' + \
                   str(article_slug)[2:-2] + '\t' + str(article_url)[2:-2] + '\t' + \
                   str(article_content)[2:-2] + '\t' + json_dict + '\n '
            file.write(line)
            # html = etree.HTML(str_content)  # 解析HTML
            # paragraphs = html.xpath('//p/text()')
            # print(paragraphs)
            # for p in paragraphs:
            #     print(p)
        except NoSuchElementException:
            print('没有找到按钮')

    file.close()
    # time.sleep(300)
    # com.close_driver()
