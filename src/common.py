# coding=utf-8
"""
此文件为selenium常用方法二次封装文件
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains  # 处理鼠标事件
from selenium.webdriver.support.select import Select  # 用于处理下拉框
from selenium.common.exceptions import *  # 用于处理异常
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # 用于处理元素等待
# from PIL import Image, ImageEnhance
# import pytesseract
import time
from urllib.parse import urlparse
from src.element import Element
import re
import numpy as np
from os.path import exists
from types import ModuleType
from collections import defaultdict
from loguru import logger
from lxml.html import fromstring, HtmlElement

from src.similarity import similarity

# from src.similarity import similarity

CONTENT_EXTRACTOR_USELESS_TAGS = ['meta', 'style', 'script', 'link', 'video', 'audio', 'iframe', 'source', 'svg',
                                  'path',
                                  'symbol', 'img', 'footer', 'header']
CONTENT_EXTRACTOR_STRIP_TAGS = ['span', 'blockquote', 'font', 'sup', 'b', 'u', 'i', 'strong', 'em', 'wbr', 'h2']
CONTENT_EXTRACTOR_NOISE_XPATHS = [
    '//div[contains(@class, "comment")]',
    '//div[contains(@class, "advertisement")]',
    '//div[contains(@class, "advert")]',
    '//div[contains(@style, "display: none")]',
]
CONTENT_EXTRACTOR_USELESS_ATTR = ['font', 'class', 'style', 'size', 'face', 'color', 'align', 'lang']


def remove_element(element: Element):
    """
    remove child element from parent
    :param element:
    :return:
    """
    if element is None:
        return
    p = element.getparent()
    if p is not None:
        p.remove(element)


def remove_children(element: Element, xpaths):
    """
    remove children from element
    :param element:
    :param xpaths:
    :return:
    """
    if element is None:
        return
    if not xpaths:
        return
    for xpath in xpaths:
        nodes = element.xpath(xpath)
        for node in nodes:
            remove_element(node)
    return element


def html2element(html: str):
    """
    convert html to HtmlElement
    :param html:
    :return:
    """
    if not html:
        return None
    element = fromstring(html)
    element.__class__ = Element
    return element


def file2element(file_path):
    """
    convert file to element
    :param file_path:
    :return:
    """
    if not exists(file_path):
        return
    with open(file_path, encoding='utf-8') as f:
        return html2element(f.read())


def selector(element: Element):
    """
    get id using recursive function.
    for example result: html/body/div/div/ul/li
    :param element:
    :return:
    """
    if element is None:
        return ''
    p = parent(element)
    if p is not None:
        return selector(p) + '>' + alias(element)
    return element.alias


def path_raw(element: Element):
    """
    get tag path using recursive function, only contains raw tag
    for example result: html/body/div/div/ul/li
    :param element:
    :return:
    """
    if element is None:
        return ''
    p = parent(element)
    if p is not None:
        return path_raw(p) + '/' + element.tag
    return element.tag


def path(element: Element):
    """
    get tag path using recursive function.
    for example result: html/body/div/div/ul/li
    :param element:
    :return:
    """
    if element is None:
        return ''
    result = path_raw(element)
    # get nth-child
    nth = len(list(element.itersiblings(preceding=True))) + 1
    result += f':nth-child({nth})'
    return result


def a_descendants(element: Element):
    """
    get
    :param element:
    :return:
    """
    if element is None:
        return []
    descendants = []
    for descendant in element.xpath('.//a'):
        descendant.__class__ = Element
        descendants.append(descendant)
    return descendants


def a_descendants_group(element: Element):
    """
    get linked descendants group
    :param element:
    :return:
    """
    result = defaultdict(list)
    for linked_descendant in element.a_descendants:
        p = linked_descendant.path_raw
        result[p].append(linked_descendant)
    return result


def parent(element: Element):
    """
    get parent of element
    :param element:
    :return:
    """
    if element is None:
        return None
    parent = element.getparent()
    if isinstance(parent, ModuleType):
        parent.__class__ = Element
    return parent


def children(element: Element, including=False):
    """
    get children
    :param element:
    :param including:
    :return:
    """
    if element is None:
        return []
    if including:
        yield element
    for child in element.iterchildren():
        if isinstance(child, HtmlElement):
            child.__class__ = Element
            yield child


def siblings(element: Element, including=False):
    """
    get siblings of element
    :param element:
    :param including: include current element or not
    :return:
    """
    if element is None:
        return []
    if including:
        yield element
    for sibling in element.itersiblings(preceding=True):
        if isinstance(sibling, HtmlElement):
            sibling.__class__ = Element
            yield sibling
    for sibling in element.itersiblings(preceding=False):
        if isinstance(sibling, HtmlElement):
            sibling.__class__ = Element
            yield sibling


def descendants(element: Element, including=False):
    """
    get descendants clement of specific element
    :param element: parent element
    :param including: including current element or not
    :return:
    """
    if element is None:
        return []
    if including:
        yield element
    for descendant in element.iterdescendants():
        if isinstance(descendant, HtmlElement):
            descendant.__class__ = Element
            yield descendant


def alias(element: Element):
    """
    get alias of element, concat tag and attribs
    :param element:
    :return:
    """
    if element is None:
        return ''
    tag = element.tag
    # skip nth-child
    if tag in ['html', 'body']:
        return tag
    attribs = [tag]
    for k, v in element.attrib.items():
        k, v = re.sub(r'\s*', '', k), re.sub(r'\s*', '', v)
        attribs.append(f'[{k}="{v}"]' if v else f'[{k}]')
    result = ''.join(attribs)
    # get nth-child
    nth = len(list(element.itersiblings(preceding=True))) + 1
    result += f':nth-child({nth})'
    return result


def children_of_head(element: Element):
    """
    get children element of body element
    :param element:
    :return:
    """
    if element is None:
        return []
    body_xpath = '//head'
    body_element = element.xpath(body_xpath)
    if body_element:
        body_element.__class__ = Element
        return descendants(body_element, True)
    return []


def descendants_of_body(element: Element):
    """
    get descendants element of body element
    :param element:
    :return:
    """
    if element is None:
        return []
    body_xpath = '//body'
    elements = element.xpath(body_xpath)
    if elements:
        elements[0].__class__ = Element
        return list(descendants(elements[0], True))
    return []


def text(element: Element):
    """
    get text of element
    :param element:
    :return:
    """
    if element is None:
        return 0
    text = ''.join(element.xpath('.//text()'))
    text = re.sub(r'\s*', '', text, flags=re.S)
    return text


def number_of_char(element: Element):
    """
    get number of char, for example, result of `<a href="#">hello</a>world` = 10
    :param element:
    :return: length
    """
    if element is None:
        return 0
    return len(text(element))


def number_of_a_char(element: Element):
    """
    get number of linked char, for example, result of `<a href="#">hello</a>world` = 5
    :param element:
    :return: length
    """
    if element is None:
        return 0
    text = ''.join(element.xpath('.//a//text()'))
    text = re.sub(r'\s*', '', text, flags=re.S)
    return len(text)


def number_of_a_char_log10(element: Element):
    """
    get number of linked char, to log10
    :param element:
    :return: length
    """
    if element is None:
        return 0
    return np.log10(number_of_a_char(element) + 1)


def number_of_p_children(element: Element):
    """
    get number of p tags in children
    :param element:
    :return:
    """
    if element is None:
        return 0
    return len(element.xpath('./p'))


def number_of_p_descendants(element: Element):
    """
    get number of p tags in descendants
    :param element:
    :return:
    """
    if element is None:
        return 0
    return len(element.xpath('.//p'))


def number_of_p_descendants_log10(element: Element):
    """
    get number of p tags, to log10
    :param element:
    :return:
    """
    if element is None:
        return 0
    return np.log10(number_of_p_descendants(element))


def number_of_a_descendants(element: Element):
    """
    get number of a tags in this element
    :param element:
    :return:
    """
    if element is None:
        return 0
    return len(element.xpath('.//a'))


# def number_of_punctuation(element: Element):
#     """
#     get number of punctuation of text in this element
#     :param element:
#     :return:
#     """
#     if element is None:
#         return 0
#     text = ''.join(element.xpath('.//text()'))
#     text = re.sub(r'\s*', '', text, flags=re.S)
#     punctuations = [c for c in text if c in PUNCTUATION]
#     return len(punctuations)


def number_of_descendants(element: Element):
    """
    get number of descendants
    :param element:
    :return:
    """
    if element is None:
        return 0
    # return len(element.xpath('.//*'))
    return len(list(descendants(element, including=False)))


def number_of_siblings(element: Element):
    """
    get number of siblings
    :param element:
    :return:
    """
    if element is None:
        return 0
    return len(list(siblings(element, including=False)))


# def number_of_clusters(element: Element, tags=None):
#     """
#     get number of clusters
#     :param element:
#     :return:
#     """
#     from gerapy_auto_extractor.extractors.list import LIST_MIN_NUMBER, LIST_MAX_LENGTH, LIST_MIN_LENGTH, \
#         SIMILARITY_THRESHOLD
#     if element is None:
#         return 0
#     if tags and not isinstance(tags, (list, tuple)):
#         logger.error('you must pass tags arg as list or tuple')
#     descendants_tree = defaultdict(list)
#     descendants = descendants_of_body(element)
#     for descendant in descendants:
#         # if one element does not have enough siblings, it can not become a child of candidate element
#         if descendant.number_of_siblings + 1 < LIST_MIN_NUMBER:
#             continue
#         # if min length is larger than specified max length, it can not become a child of candidate element
#         if descendant.a_descendants_group_text_min_length > LIST_MAX_LENGTH:
#             continue
#         # if max length is smaller than specified min length, it can not become a child of candidate element
#         if descendant.a_descendants_group_text_max_length < LIST_MIN_LENGTH:
#             continue
#         # descendant element must have same siblings which their similarity should not below similarity_threshold
#         if descendant.similarity_with_siblings < SIMILARITY_THRESHOLD:
#             continue
#         # filter tag
#         if tags and descendant.tag not in tags:
#             continue
#         descendants_tree[descendant.parent_selector].append(descendant)
#     return len(descendants_tree)


def number_of_children(element: Element):
    """
    get number of children
    :param element:
    :return:
    """
    if element is None:
        return 0
    return len(list(children(element)))


def density_of_text(element: Element):
    """
    get density of text, using:
               number_of_char - number_of_a_char
    result = ------------------------------------------
               number_of_descendants - number_of_a_descendants
    :return:
    """
    # if denominator is 0, just return 0
    if element.number_of_descendants - element.number_of_a_descendants == 0:
        return 0
    return (element.number_of_char - element.number_of_a_char) / \
           (element.number_of_descendants - element.number_of_a_descendants)


def density_of_punctuation(element: Element):
    """
    get density of punctuation, using
                number_of_char - number_of_linked_char
    result = -----------------------------------------
                 number_of_punctuation + 1
    :param element:
    :return:
    """
    result = (element.number_of_char - element.number_of_a_char) / \
             (element.number_of_punctuation + 1)
    # result should not be zero
    return result or 1


def similarity_with_element(element1: Element, element2: Element):
    """
    get similarity between two elements
    :param element1:
    :param element2:
    :return:
    """
    alias1 = element1.alias
    alias2 = element2.alias
    # TODO: use better metrics to compare the two elements
    return similarity(alias1, alias2)


def similarity_with_siblings(element: Element):
    """
    get similarity with siblings
    :param element:
    :return:
    """
    scores = []
    for sibling in siblings(element):
        # TODO: maybe compare all children not only alias
        scores.append(similarity_with_element(element, sibling))
    if not scores:
        return 0
    return np.mean(scores)


class Browser(object):
    # 初始化
    def __init__(self):
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')  # 上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
        # 创建浏览器
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.Chrome(chrome_options=chrome_options)
        # 浏览器最大化
        self.browser.maximize_window()

    def get_browser(self):
        return self.browser

    # 访问指定url
    def open_url(self, purl):
        self.browser.get(purl)
        self.browser.implicitly_wait(10)

    def close_driver(self):
        self.browser.quit()

    # 结束的时候清理了
    def __del__(self):
        time.sleep(3)
        self.browser.quit()


def get_element_text_or_tail_or_attr(_element, _type):
    if _type == 'text':
        _text = _element.text if _element.text else ''
        return _text
    if _type == 'tail':
        _tail = _element.tail if _element.tail else ''
        return _tail
    if _type == 'href':
        _href = _element.get('href') if _element.get('href') else ''
        return _href


class BrowserHelper(object):
    """
    selenium框架的主要类
    """
    original_window = None

    def __init__(self, browser='chrome'):
        """
        运行初始化方法默认chrome，当然，你也可以传入一个其他浏览器名称，
        """
        if browser == "firefox" or browser == "ff":
            self.driver = webdriver.Firefox()
        elif browser == "chrome":
            options = Options()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            self.driver = webdriver.Chrome(options=options)
        elif browser == "internet explorer" or browser == "ie":
            self.driver = webdriver.Ie()
        elif browser == "opera":
            self.driver = webdriver.Opera()
        elif browser == "chrome_headless":
            options = Options()
            options.add_argument('--headless')
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            self.driver = webdriver.Chrome(options=options)
        elif browser == 'edge':
            self.driver = webdriver.Edge()
        else:
            raise NameError(
                "找不到 %s 浏览器,你应该从这里面选取一个 'ie', 'ff', 'opera', 'edge', 'chrome' or 'chrome_headless'." % browser)

    def open(self, url, title='', timeout=10):
        u"""打开浏览器，并最大化，判断title是否为预期"""
        self.driver.get(url)
        # self.driver.maximize_window()
        try:
            WebDriverWait(self.driver, timeout, 1).until(ec.title_contains(title))
        except TimeoutException:
            print("open %s title error" % url)
        except Exception as msg:
            print("Error:%s" % msg)

    def find_element(self, locator, timeout=10):
        u"""定位元素，参数locator为原则"""
        try:
            element = WebDriverWait(self.driver, timeout=10.0).until(ec.presence_of_element_located(locator))
            return element
        except NoSuchElementException:
            print("%s 页面未找到元素 %s" % (self, locator))

    def find_elements(self, locator, timeout=10):
        u"""定位一组元素"""
        elements = WebDriverWait(self.driver, timeout, 1).until(ec.presence_of_all_elements_located(locator))
        return elements

    def element_wait(self, by, value, secs=5):
        """
        等待元素显示
        """
        try:
            if by == "id":
                WebDriverWait(self.driver, secs, 1).until(ec.presence_of_element_located((By.ID, value)))
            elif by == "name":
                WebDriverWait(self.driver, secs, 1).until(ec.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                WebDriverWait(self.driver, secs, 1).until(ec.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "link_text":
                WebDriverWait(self.driver, secs, 1).until(ec.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "xpath":
                WebDriverWait(self.driver, secs, 1).until(ec.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                WebDriverWait(self.driver, secs, 1).until(ec.presence_of_element_located((By.CSS_SELECTOR, value)))
            else:
                raise NoSuchElementException(
                    "找不到元素，请检查语法或元素")
        except TimeoutException:
            print("查找元素超时请检查元素")

    def get_element(self, css):
        """
        判断元素定位方式，并返回元素
        有两种判断方式，
        """
        if "=>" not in css:
            by = "css"  # 如果是css的格式是#aaa,所以在此加入判断如果不包含=>就默认是css传给上面的element_wait判断元素是否存在
            value = css
            # wait element.
            self.element_wait(by, css)
        else:
            by = css.split("=>")[0]
            value = css.split("=>")[1]
            if by == "" or value == "":
                raise NameError(
                    "语法错误，参考: 'id=>kw 或 xpath=>//*[@id='kw'].")
            self.element_wait(by, value)

        if by == "id":
            element = self.driver.find_element(By.ID, value)
        elif by == "name":
            element = self.driver.find_element(By.NAME, value)
        elif by == "class":
            element = self.driver.find_element(By.CLASS_NAME, value)
        elif by == "link_text":
            element = self.driver.find_element(By.LINK_TEXT, value)
        elif by == "xpath":
            element = self.driver.find_element(By.XPATH, value)  # 如果是xpath要以此格式传入xpath=>//*[@id='su']
        elif by == "css":
            element = self.driver.find_element(By.CSS_SELECTOR, value)
        else:
            raise NameError(
                "Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
        return element

    def get_elements(self, css):
        """
        判断元素定位方式，并返回元素
        """
        if "=>" not in css:
            by = "css"  # 如果是css的格式是#aaa,所以在此加入判断如果不包含=>就默认是css传给上面的element_wait判断元素是否存在
            value = css
            # wait element.
            self.element_wait(by, css)
        else:
            by = css.split("=>")[0]
            value = css.split("=>")[1]
            if by == "" or value == "":
                raise NameError(
                    "语法错误，参考: 'id=>kw 或 xpath=>//*[@id='kw'].")
            self.element_wait(by, value)

        if by == "id":
            elements = self.driver.find_elements(By.ID, value)
        elif by == "name":
            elements = self.driver.find_elements(By.NAME, value)
        elif by == "class":
            elements = self.driver.find_elements(By.CLASS_NAME, value)
        elif by == "link_text":
            elements = self.driver.find_elements(By.LINK_TEXT, value)
        elif by == "xpath":
            elements = self.driver.find_elements(By.XPATH, value)  # 如果是xpath要以此格式传入xpath=>//*[@id='su']
        elif by == "css":
            elements = self.driver.find_elements(By.CSS_SELECTOR, value)
        else:
            raise NameError(
                "Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
        return elements

    def click(self, locator):
        u"""封装点击操作"""
        element = self.find_element(locator)
        element.click()

    def send_key(self, locator, text):
        u"""发送文本后清除内容"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def is_text_in_element(self, text, locator, timeout=10):
        u"""判断是否定位到元素"""
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(ec.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            print(u"元素未定位到:" + str(locator))
            return False
        else:
            return result

    def is_title(self, title, timeout=10):
        u"""判断title完全相等"""
        result = WebDriverWait(self.driver, timeout, 1).until(ec.title_is(title))
        return result

    def is_title_contains(self, title, timeout=10):
        u"""判断是否包含title"""
        result = WebDriverWait(self.driver, timeout, 1).until(ec.title_contains(title))
        return result

    def is_select(self, locator, timeout=10):
        u"""判断元素是否被选中"""
        result = WebDriverWait(self.driver, timeout, 1).until(ec.element_located_to_be_selected(locator))
        return result

    def is_select_be(self, locator, timeout=10, selected=True):
        u"""判断元素的状态"""
        return WebDriverWait(self.driver, timeout, 1).until(ec.element_located_selection_state_to_be(locator, selected))

    def is_alert_present(self, timeout=10):
        u"""判断页面有无alert弹出框，有alert返回alert，无alert返回FALSE"""
        try:
            return WebDriverWait(self.driver, timeout, 1).until(ec.alert_is_present())
        except:
            print("No Alert Present")

    def is_visibility(self, locator, timeout=10):
        u"""判断元素是否可见，可见返回本身，不可见返回FALSE"""
        return WebDriverWait(self.driver, timeout, 1).until(ec.visibility_of_element_located(locator))

    def is_invisibility(self, locator, timeout=10):
        u"""判断元素是否可见，不可见，未找到元素返回True"""
        return WebDriverWait(self.driver, timeout, 1).until(ec.invisibility_of_element_located(locator))

    def is_clickable(self, locator, timeout=10):
        u"""判断元素是否可以点击，可以点击返回本身，不可点击返回FALSE"""
        return WebDriverWait(self.driver, timeout, 1).until(ec.element_to_be_clickable(locator))

    def is_located(self, locator, timeout=10):
        u"""判断元素是否定位到（元素不一定是可见），如果定位到返回Element，未定位到返回FALSE"""
        return WebDriverWait(self.driver, timeout, 1).until(ec.presence_of_element_located(locator))

    def move_is_element(self, locator):
        u"""鼠标悬停操作"""
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def back(self):
        u"""返回到旧的窗口"""
        self.driver.back()

    def forward(self):
        u"""前进到新窗口"""
        self.driver.forward()

    def close(self):
        u"""关闭窗口"""
        self.driver.close()

    def quit(self):
        u"""关闭driver和所有窗口"""
        self.driver.quit()

    def get_title(self):
        u"""获取当前窗口的title"""
        return self.driver.title

    def get_netloc(self):
        u"""获取当前窗口的title"""
        res = urlparse(self.driver.current_url)
        return res.scheme + "://" + res.netloc

    def is_netloc(self, url: str) -> bool:
        res = urlparse(url)
        if res.netloc == "":
            return True
        return False

    def get_current_url(self):
        u"""获取当前页面url"""
        return self.driver.current_url

    def get_text(self, locator):
        u"""获取文本内容"""
        return self.find_element(locator).text

    def get_browser_log_level(self):
        u"""获取浏览器错误日志级别"""
        lists = self.driver.get_log('browser')
        list_value = []
        if lists.__len__() != 0:
            for dicts in lists:
                for key, value in dicts.items():
                    list_value.append(value)
        if 'SEVERE' in list_value:
            return "SEVERE"
        elif 'WARNING' in list_value:
            return "WARNING"
        return "SUCCESS"

    def get_attribute(self, locator, name):
        u"""获取属性"""
        return self.find_element(locator).get_attribute(name)

    def js_execute(self, js):
        u"""执行js"""
        return self.driver.execute_script(js)

    def js_fours_element(self, locator):
        u"""聚焦元素"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def js_scroll_top(self):
        u"""滑动到页面顶部"""
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self):
        u"""滑动到页面底部"""
        js = "window.scrollTo(0, document.body.scrollHeight)"
        self.driver.execute_script(js)

    def select_by_index(self, locator, index):
        u"""通过所有index，0开始,定位元素"""
        element = self.find_element(locator)
        Select(element).select_by_index(index)

    def select_by_value(self, locator, value):
        u"""通过value定位元素"""
        element = self.find_element(locator)
        Select(element).select_by_value(value)

    def select_by_text(self, locator, text):
        u"""通过text定位元素"""
        element = self.find_element(locator)
        Select(element).select_by_visible_text(text)

    def f5(self):
        """
        刷新当前页面.
        用法:
        driver.f5()
        """
        self.driver.refresh()

    def open_new_window(self, css):
        """
        打开新窗口并切换到新打开的窗口.
        用法:
        传入一个点击后会跳转的元素
        driver.open_new_window("link_text=>注册")
        """
        original_window = self.driver.current_window_handle
        el = self.get_element(css)
        el.click()
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != original_window:
                self.driver.switch_to.window(handle)

    # def get_verify_code(self, locator):
    #     u"""获取图片验证码"""
    #     # 验证码图片保存地址
    #     screenImg = "D:/image/verifyCode.png"
    #     # 浏览器页面截图
    #     self.driver.get_screenshot_as_file(screenImg)
    #
    #     # 定位验证码大小
    #     location = self.find_element(locator).location
    #     size = self.find_element(locator).size
    #
    #     left = location['x']
    #     top = location['y']
    #     right = location['x'] + size['width']
    #     bottom = location['y'] + size['height']
    #
    #     # 从文件读取截图，截取验证码位置再次保存
    #     img = Image.open(screenImg).crop((left, top, right, bottom))
    #     img.convert('L')  # 转换模式：L|RGB
    #     img = ImageEnhance.Contrast(img)  # 增加对比度
    #     img = img.enhance(2.0)  # 增加饱和度
    #     img.save(screenImg)
    #
    #     # 再次读取验证码
    #     img = Image.open(screenImg)
    #     time.sleep(1)
    #     code = pytesseract.image_to_string(img)
    #     return code

    def open_tab(self):
        u"""打开新选项卡并切换到新选项卡"""
        self.driver.switch_to.new_window('tab')

    def open_window(self):
        u"""打开一个新窗口并切换到新窗口"""
        self.driver.switch_to.new_window('window')

    def switch_tab_or_window(self, original_window: any):
        u"""切换回旧选项卡或窗口"""
        self.driver.switch_to.window(original_window)


if __name__ == '__main__':
    driver = BrowserHelper("chrome")
    # 检查是否处理反爬
    driver.open("https://bot.sannysoft.com/")
