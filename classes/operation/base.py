# -*- encoding: utf-8 -*-
"""
@File    :   base.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/9 15:52   JeasonZhang      1.0         None
"""
import abc

import pandas as pd
from pandas import DataFrame

from classes.browser import Browser


class Operation:
    __metaclass__ = abc.ABCMeta
    browser = Browser()

    def __init__(self, president: str):
        self.output_df = DataFrame()
        self.president = president
        self.index_list: list[int] = []
        self.date_list: list[str] = []
        self.president_list: list[str] = []
        self.article_short_url_list: list[str] = []
        self.article_url_list: list[str] = []
        self.article_html_list: list[str] = []
        self.article_content_list: list[str] = []
        self.president_spec_content_list: list[dict] = []

    def __del__(self):
        Operation.browser.quit()

    @abc.abstractmethod
    def run(self):
        return

    @abc.abstractmethod
    def get_article_urls(self):
        return

    @abc.abstractmethod
    def get_article_html(self):
        return

    @abc.abstractmethod
    def extract_article_content(self):
        return

    def save_result(self):
        # Save the metadata to an HDF5 file
        with pd.HDFStore(f'./{self.president}.h5') as store:
            store.put('data', self.output_df, format='table')
            store.get_storer('data').attrs.metadata = self.output_df.attrs
        # self.output_df.to_pickle(f'./{self.president}.pkl.bz2')

    def read_result(self, filename):
        # Read the metadata and DataFrame from the HDF5 file
        with pd.HDFStore(filename) as store:
            metadata = store.get_storer('data').attrs.metadata
            df = store.get('data')
            self.output_df = df
