# -*- encoding: utf-8 -*-
"""
@File    :   record.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/9 15:58   JeasonZhang      1.0         None
"""
from dataclasses import dataclass
from pandas_dataclasses import AsFrame, Index, Data
from typing import Annotated as Ann
# Record = make_dataclass("Record", [
#     ("date", date),
#     ("president", str),
#     ("article_link", str),
#     ("article_html", str),
#     ("article_content", str),
#     ('president_spec_content', dict)])


@dataclass
class Record(AsFrame):
    index: Ann[Index[int], 'index'] = 0
    date_: Ann[Data[str], 'date'] = ''
    president: Data[str] = ''
    article_link: Data[str] = ''
    article_short_link: Data[str] = ''
    article_html: Data[str] = ''
    article_content: Data[str] = ''
    president_spec_content: Data[str] = ''

    # @property
    # def president_spec_content(self):
    #     return self.__president_spec_content
    #
    # @president_spec_content.setter
    # def president_spec_content(self, content: dict):
    #     self.__president_spec_content = str(content)
