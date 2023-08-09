# -*- encoding: utf-8 -*-
"""
@File    :   main.py
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2021

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/11/1 23:34   JeasonZhang      1.0         None
"""
import re
import time
from html import unescape

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from lxml import etree
from utils.element import remove_children, children, remove_element, html2element
from classes.browser import Browser
from classes.element import Element
from utils.element import get_element_text_or_tail_or_attr
from utils.element import CONTENT_EXTRACTOR_USELESS_TAGS, CONTENT_EXTRACTOR_STRIP_TAGS, CONTENT_EXTRACTOR_NOISE_XPATHS, \
    CONTENT_EXTRACTOR_USELESS_ATTR


def preprocess4content_extractor(element: Element):
    """
    preprocess element for content extraction
    :param element:
    :return:
    """
    # 将该标签内所有内容全部移除，包括子元素
    etree.strip_elements(element, *CONTENT_EXTRACTOR_USELESS_TAGS)
    # 只移除该标签，但是保留该标签下面的子标签
    etree.strip_tags(element, *CONTENT_EXTRACTOR_STRIP_TAGS)

    remove_children(element, CONTENT_EXTRACTOR_NOISE_XPATHS)

    etree.strip_attributes(element, *CONTENT_EXTRACTOR_USELESS_ATTR)


def process4content_extractor(tag_set, date_set, element: Element, date_):
    # print(len(list(children(element))))
    for child in children(element):
        # 把div节点转换成p节点
        if child.tag.lower() == 'div':
            child.tag = 'p'
        if child.tag != 'p':  # 不是p标签
            tag_set.add(child.tag)
            date_set.add(date_)
            # print(date_ + '\t' + child.tag)
            # print(len(list(children(child))))
    p_tag_list = element.xpath('/html/div/p')
    for p_tag in p_tag_list:
        if (p_tag.text in ["b' ", ' ', '', "b'"]) and (p_tag.tail in [' ', '', '  ']):
            remove_element(p_tag)
        pp_tag_list = p_tag.xpath('//p')
        if pp_tag_list:
            if (p_tag.text in [' ', '']) and (p_tag.tail in [' ', '']):
                remove_element(p_tag)


def build_month_url_list():
    url_list = [
        'https://2009-2017.state.gov/r/pa/prs/appt/2009appt/index.htm',
    ]
    for i in range(10, 17):
        for j in range(1, 13):
            url = 'https://2009-2017.state.gov/r/pa/prs/appt/20' + str(i).zfill(2) + '/' + str(j).zfill(
                2) + '/index.htm'
            url_list.append(url)
    url_list.append('https://2009-2017.state.gov/r/pa/prs/appt/2017/index.htm')
    return url_list


def get_obama_day_url(browser, filename):
    month_url_list = build_month_url_list()
    output_link_obama = open(filename, 'w+', encoding='utf8')
    for month_url in month_url_list:
        if month_url == 'https://2009-2017.state.gov/r/pa/prs/appt/2010/08/index.htm':
            month_url = 'https://2009-2017.state.gov/r/pa/prs/appt/2010/c38444.htm'
        elif month_url == 'https://2009-2017.state.gov/r/pa/prs/appt/2016/11/index.htm':
            month_url = 'https://2009-2017.state.gov/r/pa/prs/appt/2016/c73595.htm'
        elif month_url == 'https://2009-2017.state.gov/r/pa/prs/appt/2016/12/index.htm':
            month_url = 'https://2009-2017.state.gov/r/pa/prs/appt/2016/c74062.htm'
        browser.open(month_url)
        link_elements = browser.find_elements((By.XPATH, '//div[@class="l-wrap"]//a'))
        for link_element in link_elements:
            replace_str_list = [
                '*', '-', 'for', ':', 'REVISED', 'UPDATED', 'Revised',
                'Daily Appointments Schedule', 'Daily Appoinments Schedule', 'Daily appointments Schedule',
                'Daily Appointsments Schedule', 'Public Appointments Schedule',
                'Public Schedule', 'Pubilc Schedule', 'Public schedule'
            ]
            date_str = str(link_element.text).replace('  ', ' ')
            link_address = str(link_element.get_attribute('href'))
            for replace_str in replace_str_list:
                date_str = date_str.replace(replace_str, '')
            date_str = date_str.strip()
            try:
                if date_str == 'May 6 2012':
                    date_str = 'May 6, 2012'
                struct_time = time.strptime(date_str, "%B %d, %Y")  # March 1, 2013
                new_date = time.strftime("%Y-%m-%d", struct_time)
            except ValueError:
                year = link_address.split('/')[-3] if link_address.split('/')[-3] != '2009appt' else '2009'
                # month = link_address.split('/')[-2]
                date_str = date_str + ', ' + year
                struct_time = time.strptime(date_str, "%B %d %A, %Y")  # April 30  Tuesday, 2013
                new_date = time.strftime("%Y-%m-%d", struct_time)
            line = new_date + '\t' + link_address + '\n'
            output_link_obama.write(line)
            print(line)
    output_link_obama.close()


def main():
    browser = Browser()
    output_obama_day_link_filename = 'obama_link.txt'
    get_obama_day_url(browser, output_obama_day_link_filename)
    output_obama_html_filename = 'obama_html.txt'
    output_bush_html = open(output_obama_html_filename, 'w+', encoding='utf8')
    for line in open(output_obama_day_link_filename, 'r'):
        date = line.split('\t')[0]
        link = line.split('\t')[1]
        browser.open(link)
        day_content_element = browser.find_element((By.XPATH, '//*[@id="centerblock"]'))
        # origin_html = day_content_element.text.replace('\n', ';;;;')
        html = day_content_element.get_attribute("innerHTML")
        html = html.replace('\t', '').replace('\n', '').replace('&nbsp;', '').replace('<p></p>', '')
        line = date + '\t' + html + '\n'
        output_bush_html.write(line)
    output_bush_html.close()
    browser.close()

    output_file_html = open('obama_html_preprocess.txt', 'w+', encoding='utf8')
    tag_set = set()
    date_set = set()
    for line in open('obama_html.txt', 'r+', encoding='utf8'):
        line = line.replace('\n', '')
        date = line.split('\t')[0]
        html = line.split('\t')[1]
        soup = BeautifulSoup(html, 'lxml')
        fixed_html_bytes = soup.prettify(encoding='utf8', formatter='minimal')
        fixed_html_str = str(fixed_html_bytes)
        fixed_html_str = fixed_html_str.replace('\\n', ' ') \
            .replace('<br style="mso-special-character: line-break"/>', ';;;;') \
            .replace('<br clear="all" style="page-break-before: always; mso-special-character: line-break"/>', ';;;;') \
            .replace('<br clear="all" style="page-break-before: always"/>', ';;;;') \
            .replace('<br clear="all"/>', ';;;;').replace('<br style=""/>', ';;;;') \
            .replace('<br/>', ';;;;')
        fixed_html_str = re.sub(' +', ' ', fixed_html_str)

        original_element = html2element(fixed_html_str)
        preprocess4content_extractor(original_element)
        process4content_extractor(tag_set, date_set, original_element, date)

        html_out = unescape(etree.tostring(original_element).decode()) \
            .replace(';;;;;;;;', ';;;;').replace(';;;;;;;;', ';;;;')
        html_out = re.sub(r'<p>\s+</p>', '', html_out)
        html_out = re.sub(r'<p>\s+</p>', '', html_out)
        html_out = re.sub(' +', ' ', html_out)
        # print(html_out)
        output_file_html.write(date + '\t' + html_out + '\n')
    print(tag_set)
    print('\n'.join(date_set))
    output_file_html.close()

    output_file = open('output_obama.txt', 'w+', encoding='utf8')
    for line in open('obama_html_preprocess.txt', 'r+', encoding='utf8'):
        line = line.replace('\n', '')
        date = line.split('\t')[0]
        html = line.split('\t')[1]
        element_div = html2element(html)

        a_tag_list = element_div.xpath('//a')
        for a_tag in a_tag_list:
            a_text = get_element_text_or_tail_or_attr(a_tag, 'text')
            link = get_element_text_or_tail_or_attr(a_tag, 'href')
            final_text = a_text + '<' + link + '>'
            a_tag.text = final_text

        text_list = element_div.xpath('//text()')
        output_line_ = ';;;;'.join(text_list)
        output_line_ = date + '\t' + output_line_ + '\n'
        output_line_ = output_line_.replace("b'", '').replace('b"', '') \
            .replace(';;;; ;;;;', ';;;;').replace(';;;; ;;;;', ';;;;').replace(';;;; ;;;;', ';;;;')

        output_file.write(output_line_)
    output_file.close()

    # all_direct_children = p_tag.getchildren()
    # p_text = get_element_text_or_tail_or_attr(p_tag, 'text')
    # for children_ in all_direct_children:
    #     children_text = get_element_text_or_tail_or_attr(children_, 'text')
    #     children_tail = get_element_text_or_tail_or_attr(children_, 'tail')
    #     if children_.tag == "a":
    #         link = get_element_text_or_tail_or_attr(children_, 'href')
    #         a_text = children_text + '<' + link + '>' + children_tail
    #         p_text += a_text
    #     else:
    #         other_text = children_text + children_tail
    #         p_text += other_text
    # etree.strip_elements(p_tag, 'a')
    # if p_tag.text != p_text:
    #     p_tag.text = p_text
    # p_tail = get_element_text_or_tail_or_attr(p_tag, 'tail')
    # if p_tag.text != '':
    #     output_line_ += p_text + p_tail + ';;;;'
    # output_line_ = line.split('\t')[0] + '\t' + output_line_ + '\n'
    # output_line_ = output_line_.replace('\u202f', '')
    # output_line_ = output_line_.replace('\xa0', '')
    # output_line_ = output_line_.replace(';;;;;;;;', ';;;;')
    # return output_line_


if __name__ == '__main__':
    main()
