# -*- encoding: utf-8 -*-
"""
@File    :   main.py
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2021

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/11/4 16:39   JeasonZhang      1.0         None
"""

import time
from selenium.webdriver.common.by import By
import re

def get_month_link_list():
    year_link_list = [
        'https://2001-2009.state.gov/r/pa/prs/appt/2009/index.htm',
        'https://2001-2009.state.gov/r/pa/prs/appt/2008/index.htm',
        'https://2001-2009.state.gov/r/pa/prs/appt/2007/index.htm',
        'https://2001-2009.state.gov/r/pa/prs/appt/2006/index.htm',
        'https://2001-2009.state.gov/r/pa/prs/appt/2005/index.htm',
        'https://2001-2009.state.gov/r/pa/prs/appt/c11024.htm',
        'https://2001-2009.state.gov/r/pa/prs/appt/2003/index.htm',
        'https://2001-2009.state.gov/r/pa/prs/appt/2002/index.htm',
        'https://2001-2009.state.gov/r/pa/prs/appt/2001/index.htm'
    ]
    _month_link_list = []
    for year_link in year_link_list:
        bh.open(year_link)
        if year_link == year_link_list[0]:
            month_list = ['January']
        elif year_link == year_link_list[-1]:
            month_list = [
                'December', 'November', 'October', 'September', 'August', 'July',
                'June', 'May',
            ]
        else:
            month_list = [
                'December', 'November', 'October', 'September', 'August', 'July',
                'June', 'May', 'April', 'March', 'February', 'January',
            ]
        for month in month_list:
            month_link_element = bh.find_element((By.LINK_TEXT, month))
            _month_link_list.append(str(month_link_element.get_attribute('href')))  # 获取每个月的链接
    return _month_link_list


def get_day_link_text(_output_file_name, _month_link_list):
    output_file = open(_output_file_name, 'w+')
    for month_link in _month_link_list:
        list11 = month_link.split('/')
        year = list11[7]
        if year.__contains__('htm'):
            year = '2004'
        print(year)
        bh.open(month_link)
        day_link_td = bh.find_element((By.XPATH, '/html/body/table[2]/tbody/tr[2]/td[3]'))
        day_link_elements = day_link_td.find_elements(By.TAG_NAME, 'a')
        for day_link in day_link_elements:
            link_address = day_link.get_attribute('href')
            _output_line = year + '\t' + link_address + '\n'
            # print(_output_line)
            output_file.write(_output_line)
    output_file.close()


if __name__ == '__main__':
    # bh = BrowserHelper()
    # output_file_name_bush_link = 'bush_day_link.txt'
    # month_link_list = get_month_link_list()
    # get_day_link_text(output_file_name_bush_link, month_link_list)
    #
    # output_file_name_bush_html = 'bush_html.txt'
    # output_bush_html = open(output_file_name_bush_html, 'w+', encoding='utf8')
    # for line in open(output_file_name_bush_link, 'r'):
    #     year = line.split('\t')[0]
    #     link = line.split('\t')[1]
    #     bh.open(link)
    #     day_content_element = bh.find_element((By.XPATH, '/html/body/table[2]/tbody/tr/td'))
    #     origin_html = day_content_element.text.replace('\n', ';;;;')
    #     print(origin_html)
    #     output_bush_html.write(year + '\t' + origin_html + '\n')
    # output_bush_html.close()
    # bh.close()

    new_html_file = open('bush_html_new.txt', 'w+', encoding='utf8')
    for line in open('bush_html.txt', encoding='utf8'):
        line = line.replace(';;;;;;;;', ';;;;').replace(';;;;;;;;', ';;;;')
        year = line.split('\t')[0]
        line_list = line.split(';;;;')
        patten = r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(' \
                 r'?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2})\,\s+(\d{4})'
        str1 = re.search(patten, line)
        if str1 is not None:
            struct_time = time.strptime(str1.group(0), "%B %d, %Y")  # March 1, 2013
        else:
            patten1 = r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(' \
                      r'?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2})'
            str2 = re.search(patten1, line).group(0)
            struct_time = time.strptime(str2 + ', ' + year, "%B %d, %Y")  # March 1, 2013
        new_date = time.strftime("%Y-%m-%d", struct_time)
        print(new_date)
        new_html_file.write(new_date + '\t' + line.split('\t')[1])





