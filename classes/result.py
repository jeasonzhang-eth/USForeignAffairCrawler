# -*- encoding: utf-8 -*-
"""
@File    :   result.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/10 17:10   JeasonZhang      1.0         None
"""
from datetime import date
from .record import Record


class Result:
    """
        结果的格式为：
        date
            Record
                president
                article_short_url
                article_url
                article_html
                article_content
                president_spec_content
        date
            Record
                president
                article_short_url
                article_url
                article_html
                article_content
                president_spec_content
    """

    def __int__(self):
        self.result: dict[date, Record] = {}

        # self.index_list: list[int] = []
        # self.date_list: list[str] = []
        #
        # self.president_list: list[str] = []
        # self.article_short_url_list: list[str] = []
        # self.article_url_list: list[str] = []
        # self.article_html_list: list[str] = []
        # self.article_content_list: list[str] = []
        # self.president_spec_content_list: list[dict] = []
