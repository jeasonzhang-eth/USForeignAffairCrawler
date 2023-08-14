# -*- encoding: utf-8 -*-
"""
@File    :   base.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/9 15:52   JeasonZhang      1.0         None
"""
from __future__ import annotations

import abc
import pandas as pd
from pandas import DataFrame
from classes.browser import Browser
from datetime import date
from classes.record import Record
import pickle

Result = dict[date, Record]


class Operation:
    __metaclass__ = abc.ABCMeta
    __browser = Browser()
    __output_df: DataFrame | None = None
    __result: Result = {}
    __record_list: list[Record] = []

    @property
    def browser(self):
        return self.__browser

    @property
    def output_df(self):
        return self.__output_df

    @output_df.setter
    def output_df(self, value):
        self.__output_df = value

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, value):
        self.__result = value

    @property
    def record_list(self):
        return self.__record_list

    @record_list.setter
    def record_list(self, value):
        self.__record_list = value

    def __init__(self, president: str):
        self.president = president

        # self.index_list: list[int] = []
        # self.date_list: list[str] = []
        # self.president_list: list[str] = []
        # self.article_short_url_list: list[str] = []
        # self.article_url_list: list[str] = []
        # self.article_html_list: list[str] = []
        # self.article_content_list: list[str] = []
        # self.president_spec_content_list: list[dict] = []

    def __del__(self):
        if self.__browser:
            self.__browser.quit()

    @abc.abstractmethod
    def run(self, browser):
        return

    @abc.abstractmethod
    def get_article_urls(self, browser):
        return

    @abc.abstractmethod
    def get_article_html(self, browser):
        return

    @abc.abstractmethod
    def extract_article_content(self):
        return

    def build_result(self):
        for index, record in enumerate(self.record_list):
            self.result[record.date_] = record

    # 把result转换为DataFrame
    def to_df(self):
        self.output_df = Record.new(self.record_list)

    def save_result(self):
        # 将result保存为pickle文件
        with open(f'./{self.president}.pkl', 'wb') as f:
            pickle.dump(self.result, f)

        # 把result转换为DataFrame
        self.to_df()
        # 把dataframe及其元数据保存为HDF5文件
        with pd.HDFStore(f'./{self.president}.h5') as store:
            if self.output_df:
                store.put('data', self.output_df, format='table')
                store.get_storer('data').attrs.metadata = self.output_df.attrs
                # self.output_df.to_pickle(f'./{self.president}.pkl.bz2')

    def read_result(self):
        # 从pickle中将结果还原为result
        with open(f'./{self.president}.pkl', 'rb') as f:
            self.result = pickle.load(f)
        # 从HDF5文件中读取dataframe及其元数据
        with pd.HDFStore(f'./{self.president}.h5') as store:
            metadata = store.get_storer('data').attrs.metadata
            self.output_df = store.get('data')
            return metadata
