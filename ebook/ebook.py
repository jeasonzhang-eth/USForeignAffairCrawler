# -*- encoding: utf-8 -*-
"""
@File    :   ebook.py
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2021

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/5/7 15:10   JeasonZhang      1.0         None
"""
import time

from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from classes.browser import Browser
from utils.element_operation import get_element_text_or_tail_or_attr
from lxml.html import fromstring
# from lxml import etree


def get_article_links():
    browser = Browser()
    href_list = []
    for i in range(1, 10):
        browser.open(f'https://www.tianlangbooks.com/articles/page/{i}')
        link_elements = browser.find_elements((By.XPATH, '//*[@id="main-wrap-left"]/div[2]/article/a'))
        for link_element in link_elements:
            link = link_element.get_attribute("href")
            href_list.append(link)
    all_link = '\n'.join(href_list)
    with open('article_links_part4.txt', 'w+', encoding='utf8') as f:
        f.write(all_link)
    browser.close()


def get_lanzou_link_and_passwd():
    browser = Browser()
    with open('pan_link_part4.txt', 'w+', encoding='utf8') as f:
        for line in open("article_links_part4.txt", 'r+', encoding='utf8'):
            try:
                browser.open(line)
                input_box = browser.find_element((By.ID, 'pwbox'))
                input_box.send_keys('359198')
                button = browser.find_element((By.XPATH, '//form/button[@value="提交"]'))
                button.click()
                content_element = browser.find_element((By.CLASS_NAME, 'secret-password-content'))
                html = content_element.get_attribute('innerHTML')
                selector = fromstring(html)
                a_tag_list = selector.xpath('//p/a')
                for a in a_tag_list:
                    link = get_element_text_or_tail_or_attr(a, 'href')
                    a_text = get_element_text_or_tail_or_attr(a, 'text')
                    browser.open(link)
                    time.sleep(2)
                    output_line = f'{a_text}\t{browser.get_current_url()}\n'
                    print(output_line)
                    f.write(output_line)
            except TimeoutException or ElementClickInterceptedException:
                output_line = f'出错链接\t{line}\n'
                print(output_line)
                f.write(output_line)


if __name__ == '__main__':
    # get_article_links()
    get_lanzou_link_and_passwd()
