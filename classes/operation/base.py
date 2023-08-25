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
from typing import Union, Hashable, Any

import loguru
import pandas as pd
from pandas import DataFrame
from classes.browser import Browser
from datetime import date
from classes.record import Record
import pickle
from utils.mylogger import MyLogger

Result = dict[Union[date, str], Record]


class Operation:
    __metaclass__ = abc.ABCMeta
    __browser = Browser()
    __output_df: DataFrame | None = None
    __metadata: dict[Hashable, Any] = {}
    __result: Result = {}
    __record_list: list[Record] = []
    __logger = MyLogger().get_logger

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

    @property
    def logger(self) -> loguru._Logger:
        return self.__logger

    @logger.setter
    def logger(self, value):
        self.__logger = value

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

    @property
    def metadata(self):
        return self.__metadata

    @metadata.setter
    def metadata(self, value):
        self.__metadata = value

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

    def build_result(self, success_article_id_list):
        self.result['success_article_id_list'] = success_article_id_list
        for index, record in enumerate(self.record_list):
            # 只将成功的record计入结果
            if record.success:
                self.result[record.date_] = record

    # 把result转换为DataFrame
    def to_df(self):
        date_list: list[str] = []
        president_list: list[str] = []
        article_link_list: list[str] = []
        article_html_list: list[str] = []
        article_content_list: list[str] = []
        president_spec_content_list: list[str] = []
        success_list: list[bool] = []
        for record in self.result.values():
            if isinstance(record, Record):
                date_list.append(record.date_)
                president_list.append(record.president)
                article_link_list.append(record.article_link)
                article_html_list.append(record.article_html)
                article_content_list.append(record.article_content)
                president_spec_content_list.append(record.president_spec_content)
                success_list.append(record.success)
        self.output_df = Record.new(date_list, president_list, article_link_list, article_html_list, article_content_list, president_spec_content_list, success_list)

    def save_result(self, success_article_id_list):
        # 生成result
        self.build_result(success_article_id_list)
        # 将result保存为pickle文件
        with open(f'./{self.president}.pkl', 'wb') as f:
            pickle.dump(self.result, f)
        # 把result转换为DataFrame
        self.to_df()
        # 把dataframe及其元数据保存为HDF5文件
        with pd.HDFStore(f'./{self.president}.h5') as store:
            if not self.output_df.empty:
                store.put('data', self.output_df, format='table')
                store.get_storer('data').attrs.metadata = self.output_df.attrs

    def read_result(self) -> bool:
        try:
            # 从pickle中将结果还原为result
            with open(f'./{self.president}.pkl', 'rb') as f:
                self.result = pickle.load(f)
            # 从HDF5文件中读取dataframe及其元数据
            with pd.HDFStore(f'./{self.president}.h5') as store:
                self.metadata = store.get_storer('data').attrs.metadata
                self.output_df = store.get('data')
            return True

        except FileNotFoundError as e:
            self.logger.error(f'{e.filename}文件不存在')
            return False
