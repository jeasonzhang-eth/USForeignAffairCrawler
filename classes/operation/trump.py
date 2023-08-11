# -*- encoding: utf-8 -*-
"""
@File    :   trump.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/9 15:53   JeasonZhang      1.0         None
"""
from classes.operation.base import Operation


class OperationTrump(Operation):
    def get_article_urls(self, browser):
        pass

    def get_article_html(self, browser):
        pass

    def extract_article_content(self):
        pass

    def run(self, browser):
        pass

    def __init__(self):
        super().__init__('biden')
        return
