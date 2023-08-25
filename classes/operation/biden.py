# -*- encoding: utf-8 -*-
"""
@File    :   biden.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/9 15:53   JeasonZhang      1.0         None
"""
# from html import unescape

from lxml import etree
from lxml.html import fromstring
from selenium.webdriver.common.by import By
from classes.browser import Browser
from classes.operation.base import Operation
from classes.record import Record
from utils.element_operation import get_element_text_or_tail_or_attr
from utils.tools import format_date
from ast import literal_eval
from selenium.common.exceptions import TimeoutException


class OperationBiden(Operation):
    # article_id_list: list[int] = []
    success_article_id_list: list[int] = []

    def compare_to_last_execute(self, article_id_list: list[int]) -> tuple[bool, list[int]]:
        # 加载上一次的结果，包括result和dataframe
        has_run = self.read_result()
        if has_run:
            self.logger.info('打开上一次结果成功，此次运行不是第一次运行')
        else:
            self.logger.info('打开上一次结果失败，此次运行是第一次运行')
        # 判断字典是否为空
        if len(self.result) > 0:
            # 将上一次的成功结果保存
            self.success_article_id_list = list(self.result['success_article_id_list'])
            article_id_list_new = []
            for index, article_id in enumerate(article_id_list):
                # 拿上一次的article_id_list与这一次的article_id_list进行比较，
                if article_id not in self.result['success_article_id_list']:
                    # 如果上一次的结果中没有存储该id，就说明该id对应的文章没有下载，将其存入article_id_list_new
                    article_id_list_new.append(article_id)
            # 判断article_id_list_new的长度，如果为0，说明没有需要下载的文章
            if len(article_id_list_new) == 0:
                return False, article_id_list
            # 如果不为0，则需要进行下载，将article_id_list_new返回
            else:
                return True, article_id_list_new
        else:
            # 如果为空，说明之前没有运行过，第一次运行将原数组原封不动传回
            return True, article_id_list

    def get_article_urls(self, browser: Browser) -> bool:
        base_url = 'https://www.state.gov/public-schedule/'
        browser.open(base_url)

        article_id_text = browser.find_element((By.CSS_SELECTOR, "#post-22944")).get_attribute("data-returned-posts")
        article_id_list = article_id_text.replace('[', '').replace(']', '').split(',')
        # 与上一次运行的结果进行比较，确定是否需要继续执行
        should_continue, article_id_list = self.compare_to_last_execute(article_id_list)
        # article_id_list = [469822, 469589, 469055]
        if should_continue:
            for index, article_id in enumerate(article_id_list):
                record = Record()
                record.president = 'biden'
                article_short_link = f'https://www.state.gov/?p={article_id}'  # 这里是文章的短链接，可能失效
                record.president_spec_content = str({'article_short_link': article_short_link,  # 拜登的文章有短连接
                                                     'article_id': article_id})  # 当前这篇文章的ID
                self.record_list.append(record)
            # self.article_id_list = article_id_list
            return True
        else:
            # 如果compare_to_last_execute函数返回的结果为FALSE，则结束程序
            return False

    def get_article_html(self, browser: Browser):
        for index, record in enumerate(self.record_list):
            president_spec_content = literal_eval(record.president_spec_content)
            article_short_link = president_spec_content['article_short_link']
            article_id = president_spec_content['article_id']
            # 获取真实的文章链接
            browser.open(article_short_link)
            record.article_link = browser.get_current_url()
            try:
                # 获取标题
                title = browser.find_element((By.XPATH, '//section/div[2]/div/h1')).text
                # 从标题里获取日期
                date_text = title.replace('Public Schedule – ', '').replace('Public Schedule: ', '')
                date_text_formatted = format_date(date_text)
                record.date_ = date_text_formatted

                # 获取文章的html
                html = browser.find_element((By.CLASS_NAME, 'entry-content')).get_attribute('innerHTML')
                record.article_html = html
                # 执行到这里，说明该文章已经被抓取下来了
                self.success_article_id_list.append(article_id)
                record.success = True
            except TimeoutException as e:
                record.success = False
                self.logger.error(f'超时了，超时链接是{article_short_link}\t{e.msg}\t{e.screen}\t{e.stacktrace}')

    def extract_article_content(self):
        for index, record in enumerate(self.record_list):
            if record.success:
                output_line = ''
                selector = fromstring(record.article_html)
                p_tag_list = selector.xpath('//p')
                for p_tag in p_tag_list:
                    etree.strip_tags(p_tag, 'strong', 'u', 'b', 'span', 'em', 'script')
                    all_direct_children = p_tag.getchildren()
                    p_text = get_element_text_or_tail_or_attr(p_tag, 'text')
                    for children in all_direct_children:
                        children_text = get_element_text_or_tail_or_attr(children, 'text')
                        children_tail = get_element_text_or_tail_or_attr(children, 'tail')
                        if children.tag == "a":
                            link = get_element_text_or_tail_or_attr(children, 'href')
                            a_text = children_text + '<' + link + '>' + children_tail
                            p_text += a_text
                        elif children.tag == "br":
                            p_text += ';;;;'
                        else:
                            other_text = children_text + children_tail
                            p_text += other_text
                    etree.strip_elements(p_tag, 'a', 'br')
                    p_tag.text = p_text
                    p_tail = get_element_text_or_tail_or_attr(p_tag, 'tail')
                    if p_tail == '\n':
                        p_tail = ''
                    if p_tag.text != '':
                        output_line += p_text + p_tail + ';;;;'
                # soup = BeautifulSoup(html, 'lxml')
                # text = '\n'.join(selector.xpath('//p/text()'))
                # etree.dump(selector, pretty_print=True)
                # print(text)
                # html_out = unescape(etree.tostring(selector).decode())
                # print(count)
                # print(html_out)
                # output_file_html.write(html_out + '\n')
                # output_line = output_line + '\n'
                output_line = output_line.replace('\u202f', '')
                output_line = output_line.replace('\xa0', '')
                output_line = output_line.replace(';;;;;;;;;;;;', ';;;;')
                record.article_content = output_line
            else:
                record.article_content = ''

    def run(self, browser: Browser):
        should_continue = self.get_article_urls(browser)
        if should_continue:
            self.get_article_html(browser)
            self.extract_article_content()
            self.save_result(self.success_article_id_list)
        else:
            self.logger.info('本次运行没有需要更新的文章')

    def __init__(self):
        super().__init__('biden')
        return
