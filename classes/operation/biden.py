# -*- encoding: utf-8 -*-
"""
@File    :   biden.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/9 15:53   JeasonZhang      1.0         None
"""
from selenium.webdriver.common.by import By

from classes.operation.base import Operation
from utils.tools import format_date


class OperationBiden(Operation):
    def compare_to_last_execute(self):
        pass

    def get_article_urls(self):
        base_url = 'https://www.state.gov/public-schedule/'
        self.browser.open(base_url)
        article_count = self.browser.find_element((By.CLASS_NAME, "collection-info__number")).text

        article_id_text = self.browser.find_element((By.CSS_SELECTOR, "#post-22944")).get_attribute("data-returned-posts")
        article_id_list = article_id_text.replace('[', '').replace(']', '').split(',')

        for index, article_id in enumerate(article_id_list):
            self.index_list.append(index)
            self.article_short_url_list.append(f'https://www.state.gov/?p={article_id}')  # 这里是文章的短链接，可能失效
            self.president_spec_content_list.append({'article_count': article_count,  # 文章的数量，根据数量可以进行判断需不需要更新
                                                     'article_id': article_id})  # 当前这篇文章的ID

    def get_article_html(self):
        for index, article_link in enumerate(self.article_short_url_list):
            # 获取真实的文章链接
            self.browser.open(article_link)
            self.article_url_list.append(self.browser.get_current_url())

            # 获取日期
            title = self.browser.find_element((By.CLASS_NAME, 'featured-content__headline stars-above'))
            date_text = title.replace('Public Schedule – ', '').replace('Public Schedule: ', '')
            date_text_formatted = format_date(date_text)
            self.date_list.append(date_text_formatted)

            # 获取文章的html
            html = self.browser.find_element((By.CLASS_NAME, 'entry-content')).get_attribute('innerHTML')
            self.article_html_list[index] = html

    def extract_article_content(self):
        for index, article_html in enumerate(self.article_html_list):
            pass

    def run(self):
        self.get_article_urls()
        self.get_article_html()
        self.extract_article_content()

    def __init__(self):
        super().__init__('biden')
        return
