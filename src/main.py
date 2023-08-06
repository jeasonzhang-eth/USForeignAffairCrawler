import dataclasses

from selenium.webdriver.common.by import By

from src.president.biden.main import get_article_url
from src.common import Browser
import abc
import pandas as pd
from pandas import DataFrame
from dataclasses import dataclass
from datetime import date
from pandas_dataclasses import AsFrame, Attr, Data, Index
from tools import format_date


# Record = make_dataclass("Record", [
#     ("date", date),
#     ("president", str),
#     ("article_link", str),
#     ("article_html", str),
#     ("article_content", str),
#     ('president_spec_content', dict)])

@dataclass
class Record(AsFrame):
    index: Index[int]
    date_: Data[str]
    president: Data[str]
    article_link: Data[str]
    article_html: Data[str]
    article_content: Data[str]
    president_spec_content: Data[str]

    # @property
    # def president_spec_content(self):
    #     return self.__president_spec_content
    #
    # @president_spec_content.setter
    # def president_spec_content(self, content: dict):
    #     self.__president_spec_content = str(content)


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


class OperationBiden(Operation):
    def compare_to_last_execute(self):
        pass

    def get_article_urls(self):
        base_url = 'https://www.state.gov/public-schedule/'
        self.browser.open(base_url)
        article_count = self.browser.find_element((By.CLASS_NAME, "collection-info__number")).text

        article_id_text = self.browser.find_element((By.CSS_SELECTOR, "#post-22944")).get_attribute("data-returned-posts")
        article_id_list = article_id_text.replace('[', '').replace(']', '').split(',')

        for index, article_id in enumerate(article_id_list):
            self.index_list.append(index)
            self.article_short_url_list.append(f'https://www.state.gov/?p={article_id}')  # 这里是文章的短链接，可能失效
            self.president_spec_content_list.append({'article_count': article_count,  # 文章的数量，根据数量可以进行判断需不需要更新
                                                     'article_id': article_id})  # 当前这篇文章的ID

    def get_article_html(self):
        for index, article_link in enumerate(self.article_short_url_list):
            # 获取真实的文章链接
            self.browser.open(article_link)
            self.article_url_list.append(self.browser.get_current_url())

            # 获取日期
            title = self.browser.find_element((By.CLASS_NAME, 'featured-content__headline stars-above'))
            date_text = title.replace('Public Schedule – ', '').replace('Public Schedule: ', '')
            date_text_formatted = format_date(date_text)
            self.date_list.append(date_text_formatted)

            # 获取文章的html
            html = self.browser.find_element((By.CLASS_NAME, 'entry-content')).get_attribute('innerHTML')
            self.article_html_list[index] = html

    def extract_article_content(self):
        for index, article_html in enumerate(self.article_html_list):
            pass

    def run(self):
        self.get_article_urls()
        self.get_article_html()
        self.extract_article_content()

    def __init__(self):
        super().__init__('biden')
        return


class OperationTrump(Operation):
    def get_article_urls(self):
        pass

    def get_article_html(self):
        pass

    def extract_article_content(self):
        pass

    def run(self):
        pass

    def __init__(self):
        super().__init__('biden')
        return


class OperationObama(Operation):
    def get_article_urls(self):
        pass

    def get_article_html(self):
        pass

    def extract_article_content(self):
        pass

    def run(self):
        pass

    def __init__(self):
        super().__init__('biden')
        return


class OperationBush(Operation):
    def get_article_urls(self):
        pass

    def get_article_html(self):
        pass

    def extract_article_content(self):
        pass

    def run(self):
        pass

    def __init__(self):
        super().__init__('biden')
        return


class AbstractFactory:
    @abc.abstractmethod
    def product_operation(self, president):
        pass


class AmericaFactory(AbstractFactory):
    def product_operation(self, president):
        if president == 'biden':
            return OperationBiden()
        elif president == 'trump':
            return OperationTrump()
        elif president == 'obama':
            return OperationObama()
        elif president == 'bush':
            return OperationBush()
        else:
            raise Exception


class GermanFactory(AbstractFactory):
    def product_operation(self, president):
        pass


if __name__ == '__main__':
    operation_biden = AmericaFactory().product_operation('biden')
    operation_biden.run()
    operation_biden.browser.quit()

# def get_list(str_):
#     delete_list = [
#         '*',
#         'THE DAILY PUBLIC SCHEDULE IS SUBJECT TO CHANGE',
#     ]
#     for delete in delete_list:
#         str_ = str_.replace(delete, '')
#     list1 = str_.split('\t')
#     str_temp1 = ''
#     str_temp2 = ''
#     previous_result = True
#     para = []
#     length = len(list1[1].split(';;;;'))
#     count = 0
#
#     for line in list1[1].split(';;;;'):
#         count += 1
#         line = line.strip()
#         if line != "" and not line.startswith('('):
#             this_result = line.isupper()
#             if previous_result and this_result:  # 两次都是全大写，说明
#                 pass
#                 # str_temp = line
#                 # para.append(str_temp)
#                 # print(str_temp)
#             if previous_result and not this_result:  # 上一次是全大写，这一次不是
#                 str_temp2 = str_temp2 + ';;;;' + line
#             if not previous_result and this_result:  # 上一次不是全大写，这一次是
#                 para.append(str_temp2)
#                 str_temp2 = ''
#             if not previous_result and not this_result:  # 两次都不是全大写
#                 str_temp2 = str_temp2 + ';;;;' + line
#             if this_result:
#                 str_temp1 = line + ';;;;'
#                 str_temp2 = str_temp1 + str_temp2
#                 print(line)
#             else:
#                 print(1)
#             previous_result = this_result
#     if count == length:
#         para.append(str_temp2)
#     # print(para)
#     return para
#
#
# output_file = open('result/trump/para.txt', 'w+', encoding='utf8')
# for line1 in open('result/trump_output.txt', 'r', encoding='utf8'):
#     date = line1.split('\t')[0]
#     paras = get_list(line1)
#     for l in paras:
#         output_str = date + '\t' + l + '\n'
#         output_file.write(output_str)
# output_file.close()
