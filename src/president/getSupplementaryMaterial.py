# -*- coding: UTF-8 -*-
"""
@File    :   getSupplementaryMaterial.py
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2021

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/11/24 0:05   JeasonZhang      1.0         None
"""

import pandas as pd
from src.common import BrowserHelper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from src.common import remove_children, children, remove_element, html2element, siblings, descendants
from lxml import etree
from src.common import get_element_text_or_tail_or_attr
from src.common import CONTENT_EXTRACTOR_USELESS_TAGS, CONTENT_EXTRACTOR_STRIP_TAGS

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def process_element(element_):
    # 将该标签内所有内容全部移除，包括子标签
    etree.strip_elements(element_, *CONTENT_EXTRACTOR_USELESS_TAGS)
    # 只移除该标签，但是保留该标签下面的子标签
    etree.strip_tags(element_, *CONTENT_EXTRACTOR_STRIP_TAGS)

    a_tag_list = element_.xpath('//a')
    for a_tag in a_tag_list:
        a_text = get_element_text_or_tail_or_attr(a_tag, 'text')
        link = get_element_text_or_tail_or_attr(a_tag, 'href')
        final_text = a_text + '<' + link + '>'
        a_tag.text = final_text
    text_list = element_.xpath('//text()')

    content_ = ';;;;'.join(text_list)
    content_ = content_.replace('\n', ';;;;').replace('\t', '').replace(u'\xa0', u' ')

    # content_ = content_.encode('utf8').decode('utf8')
    print(content_)
    return content_


def preprocess_link(entity_, president_):
    # 对所有总统都需要做的操作
    entity_ = entity_.replace('<', '').replace('>', '').replace('http:', 'https:')  # 去除链接外面的<>，将http替换成https

    # 对特定总统做的操作
    if president_ == 'biden':
        pass
    elif president_ == 'trump':
        pass
    elif president_ == 'obama':
        entity_ = entity_.replace('=//', 'https://').replace('=https://', 'https://')  # 几个特例是以=开头的链接

        # 奥巴马的链接里，大部分是以//开头的，将之替换成https://
        if entity_.startswith('//'):
            entity_ = entity_.replace('//', 'https://')

        # 在奥巴马的链接里，经过上述调整后，所有链接都应该是以http开头了
        if entity_.startswith('http'):
            link_ = entity_
            # print(link_)
            return True, link_
        # 但存在一些不是链接的内容，这些内容就不做处理原路返回了
        else:
            return False, entity_
    elif president_ == 'bush':
        pass
    else:
        return "输入错误"


def get_link_content(link_, browser_, president_):
    content_ = ''
    if president_ == 'biden' or president_ == 'trump':
        if president_ == 'biden':
            prefix = 'https://www.state.gov'
        elif president_ == 'trump':
            prefix = 'https://2017-2021.state.gov'
        else:
            return '输入错误'
        if link_.startswith(prefix):
            browser_.open(link_)
            try:
                if link_.__contains__('deputy-secretary-travel') or link_.__contains__('secretary-travel'):
                    text = browser_.find_element((By.XPATH, '//div[@class="summary__list"]')).get_attribute(
                        'innerHTML')
                else:
                    text = browser_.find_element((By.XPATH, '//div[@class="entry-content"]')).get_attribute(
                        'innerHTML')
                element = html2element(text)
                content_ = process_element(element)
                print(content_)
                return content_
            except TimeoutException:
                print(link_)
                content_ = link_
                return content_
    elif president_ == 'obama':
        prefix = 'https://2009-2017.state.gov'
        if link_.startswith(prefix + '/r/pa/prs/ps'):
            print(link_)
            browser_.open(link_)
            try:
                text = browser_.find_element((By.XPATH, '//div[@id="centerblock"]')).get_attribute(
                    'innerHTML')
                # print(text)
                element = html2element(text)
                content_ = process_element(element)
                # print(content_)
                return content_

            except TimeoutException:
                print(link_)
                content_ = link_
                return content_
    elif president_ == 'bush':
        prefix = 'https://2001-2009.state.gov/'
        return content_
    else:
        return "输入错误"


def get_supplementary_material(president_):
    content_list = []
    browser = BrowserHelper()

    dataframe = pd.read_csv(f'../../../result/{president_}/{president_}_test.csv')
    link_series = dataframe['Links']

    for entity in link_series:
        # 判断存不存在网页链接
        if entity in ['None', '']:
            content_list.append('')
        # 判断是不是多个网页链接
        elif entity.startswith('['):
            link_list = eval(entity)
            new_link_list = []
            for sub_link in link_list:
                sub_link = sub_link.replace('<', '').replace('>', '')
                if sub_link.startswith('//'):
                    sub_link = sub_link.replace('//2', 'https://2')
                new_link_list.append(sub_link)
                # print(new_link_list)
            # 如果是多个链接，先不进行链接内容提取
            content_list.append('')
        else:
            # 如果既不是None，也不是空字符串，也不是链接数组，则大概率是链接，因为可能是错误的链接，所以先对链接进行预处理
            tag, link = preprocess_link(entity, president_)
            # tag为True时，说明是一个链接，tag为False时，说明不是链接
            if tag:
                # print(link.split('https://')[1].split('/')[0])  # 提取链接里的域名
                # 然后通过浏览器访问链接，拿到链接里面的文字
                # link = 'https://2009-2017.state.gov/r/pa/prs/ps/2017/01/267113.htm'
                content = get_link_content(link, browser, president_)
                content_list.append(content)
            else:
                content_list.append(link)
    print(content_list)
    if len(content_list) == link_series.__len__():
        dataframe['content'] = content_list
        dataframe.to_csv(f'{president_}_final_with_link_content.csv')
    else:
        print("长度不匹配，可能存在漏判")

    browser.close()


if __name__ == '__main__':
    president = 'obama'
    get_supplementary_material(president)
