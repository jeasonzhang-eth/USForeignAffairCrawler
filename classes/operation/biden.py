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
from classes.browser import Browser
from classes.operation.base import Operation
from classes.record import Record
from utils.tools import format_date


class OperationBiden(Operation):
    def compare_to_last_execute(self):
        pass

    def get_article_urls(self, browser: Browser):
        base_url = 'https://www.state.gov/public-schedule/'

        browser.open(base_url)
        article_count = browser.find_element((By.CLASS_NAME, "collection-info__number")).text

        article_id_text = browser.find_element((By.CSS_SELECTOR, "#post-22944")).get_attribute("data-returned-posts")
        article_id_list = article_id_text.replace('[', '').replace(']', '').split(',')

        for index, article_id in enumerate(article_id_list):
            record = Record()
            record.index = index
            record.article_short_link = f'https://www.state.gov/?p={article_id}'  # 这里是文章的短链接，可能失效
            record.president_spec_content = str({'article_count': article_count,  # 文章的数量，根据数量可以进行判断需不需要更新
                                                 'article_id': article_id})  # 当前这篇文章的ID
            self.record_list.append(record)

    def get_article_html(self, browser: Browser):
        for index, record in enumerate(self.record_list):
            # 获取真实的文章链接
            browser.open(record.article_link)
            record.article_link = browser.get_current_url()

            # 获取日期
            title = browser.find_element((By.XPATH, '//section/div[2]/div/h1')).text

            date_text = title.replace('Public Schedule – ', '').replace('Public Schedule: ', '')
            date_text_formatted = format_date(date_text)
            record.date_ = date_text_formatted

            # 获取文章的html
            html = browser.find_element((By.CLASS_NAME, 'entry-content')).get_attribute('innerHTML')
            record.article_html = html
            self.record_list[index] = record

    def extract_article_content(self):
        for index, article_html in enumerate(self.record_list):
            pass

    def run(self, browser: Browser):
        self.get_article_urls(browser)
        self.get_article_html(browser)
        self.extract_article_content()

    def __init__(self):
        super().__init__('biden')
        return
