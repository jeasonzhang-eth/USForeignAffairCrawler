# coding=utf-8
"""
此文件中保存对网页元素（Element类）的主要操作函数
"""
from lxml import etree

# from PIL import Image, ImageEnhance
# import pytesseract
from classes.browser import Browser
from classes.article_element import ArticleElement
import re
import numpy as np
from os.path import exists
from types import ModuleType
from collections import defaultdict
from lxml.html import fromstring, HtmlElement

from utils.mylogger import MyLogger
from utils.similarity import similarity

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


def remove_element(element: ArticleElement):
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


def remove_children(element: ArticleElement, xpaths):
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
    element.__class__ = ArticleElement
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


def selector(element: ArticleElement):
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


def path_raw(element: ArticleElement):
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


def path(element: ArticleElement):
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


def a_descendants(element: ArticleElement):
    """
    get
    :param element:
    :return:
    """
    if element is None:
        return []
    descendants_ = []
    for descendant in element.xpath('.//a'):
        descendant.__class__ = ArticleElement
        descendants_.append(descendant)
    return descendants_


def a_descendants_group(element: ArticleElement):
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


def parent(element: ArticleElement):
    """
    get parent of element
    :param element:
    :return:
    """
    if element is None:
        return None
    parent_: ArticleElement = element.getparent()
    if isinstance(parent_, ModuleType):
        parent_.__class__ = ArticleElement
    return parent_


def children(element: ArticleElement, including=False):
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
            child.__class__ = ArticleElement
            yield child


def siblings(element: ArticleElement, including=False):
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
            sibling.__class__ = ArticleElement
            yield sibling
    for sibling in element.itersiblings(preceding=False):
        if isinstance(sibling, HtmlElement):
            sibling.__class__ = ArticleElement
            yield sibling


def descendants(element: ArticleElement, including=False):
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
            descendant.__class__ = ArticleElement
            yield descendant


def alias(element: ArticleElement):
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


def children_of_head(element: ArticleElement):
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
        body_element.__class__ = ArticleElement
        return descendants(body_element, True)
    return []


def descendants_of_body(element: ArticleElement):
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
        elements[0].__class__ = ArticleElement
        return list(descendants(elements[0], True))
    return []


def text(element: ArticleElement):
    """
    get text of element
    :param element:
    :return:
    """
    if element is None:
        return 0
    text_ = ''.join(element.xpath('.//text()'))
    text_ = re.sub(r'\s*', '', text_, flags=re.S)
    return text_


def number_of_char(element: ArticleElement):
    """
    get number of char, for example, result of `<a href="#">hello</a>world` = 10
    :param element:
    :return: length
    """
    if element is None:
        return 0
    return len(text(element))


def number_of_a_char(element: ArticleElement):
    """
    get number of linked char, for example, result of `<a href="#">hello</a>world` = 5
    :param element:
    :return: length
    """
    if element is None:
        return 0
    text_ = ''.join(element.xpath('.//a//text()'))
    text_ = re.sub(r'\s*', '', text_, flags=re.S)
    return len(text_)


def number_of_a_char_log10(element: ArticleElement):
    """
    get number of linked char, to log10
    :param element:
    :return: length
    """
    if element is None:
        return 0
    return np.log10(number_of_a_char(element) + 1)


def number_of_p_children(element: ArticleElement):
    """
    get number of p tags in children
    :param element:
    :return:
    """
    if element is None:
        return 0
    return len(element.xpath('./p'))


def number_of_p_descendants(element: ArticleElement):
    """
    get number of p tags in descendants
    :param element:
    :return:
    """
    if element is None:
        return 0
    return len(element.xpath('.//p'))


def number_of_p_descendants_log10(element: ArticleElement):
    """
    get number of p tags, to log10
    :param element:
    :return:
    """
    if element is None:
        return 0
    return np.log10(number_of_p_descendants(element))


def number_of_a_descendants(element: ArticleElement):
    """
    get number of a tags in this element
    :param element:
    :return:
    """
    if element is None:
        return 0
    return len(element.xpath('.//a'))


def number_of_punctuation(element: ArticleElement):
    """
    get number of punctuation of text in this element
    :param element:
    :return:
    """
    if element is None:
        return 0
    text_ = ''.join(element.xpath('.//text()'))
    text_ = re.sub(r'\s*', '', text_, flags=re.S)
    PUNCTUATION = set('''！，。？、；：“”‘’《》%（）<>{}「」【】*～`,.?:;'"!%()''')
    punctuations = [c for c in text_ if c in PUNCTUATION]
    return len(punctuations)


def number_of_descendants(element: ArticleElement):
    """
    get number of descendants
    :param element:
    :return:
    """
    if element is None:
        return 0
    # return len(element.xpath('.//*'))
    return len(list(descendants(element, including=False)))


def number_of_siblings(element: ArticleElement):
    """
    get number of siblings
    :param element:
    :return:
    """
    if element is None:
        return 0
    return len(list(siblings(element, including=False)))


def number_of_clusters(element: ArticleElement, tags=None):
    """
    get number of clusters
    :param tags:
    :type tags:
    :param element:
    :return:
    """
    LIST_MIN_NUMBER = 5
    LIST_MIN_LENGTH = 8
    LIST_MAX_LENGTH = 44
    SIMILARITY_THRESHOLD = 0.8

    if element is None:
        return 0
    if tags and not isinstance(tags, (list, tuple)):
        logger = MyLogger().get_logger
        logger.error('you must pass tags arg as list or tuple')
    descendants_tree = defaultdict(list)
    descendants_ = descendants_of_body(element)
    for descendant in descendants_:
        # if one element does not have enough siblings, it can not become a child of candidate element
        if descendant.number_of_siblings + 1 < LIST_MIN_NUMBER:
            continue
        # if min length is larger than specified max length, it can not become a child of candidate element
        if descendant.a_descendants_group_text_min_length > LIST_MAX_LENGTH:
            continue
        # if max length is smaller than specified min length, it can not become a child of candidate element
        if descendant.a_descendants_group_text_max_length < LIST_MIN_LENGTH:
            continue
        # descendant element must have same siblings which their similarity should not below similarity_threshold
        if descendant.similarity_with_siblings < SIMILARITY_THRESHOLD:
            continue
        # filter tag
        if tags and descendant.tag not in tags:
            continue
        descendants_tree[descendant.parent_selector].append(descendant)
    return len(descendants_tree)


def number_of_children(element: ArticleElement):
    """
    get number of children
    :param element:
    :return:
    """
    if element is None:
        return 0
    return len(list(children(element)))


def density_of_text(element: ArticleElement):
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


def density_of_punctuation(element: ArticleElement):
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


def similarity_with_element(element1: ArticleElement, element2: ArticleElement):
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


def similarity_with_siblings(element: ArticleElement):
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


# class Browser(object):
#     # 初始化
#     def __init__(self):
#         # chrome_options = Options()
#         # chrome_options.add_argument('--headless')
#         # chrome_options.add_argument('--disable-gpu')  # 上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
#         # 创建浏览器
#         self.browser = webdriver.Chrome()
#         # self.browser = webdriver.Chrome(chrome_options=chrome_options)
#         # 浏览器最大化
#         self.browser.maximize_window()
#
#     def get_browser(self):
#         return self.browser
#
#     # 访问指定url
#     def open_url(self, purl):
#         self.browser.get(purl)
#         self.browser.implicitly_wait(10)
#
#     def close_driver(self):
#         self.browser.quit()
#
#     # 结束的时候清理了
#     def __del__(self):
#         time.sleep(3)
#         self.browser.quit()


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


if __name__ == '__main__':
    driver = Browser("chrome")
    # 检查是否处理反爬
    driver.open("https://bot.sannysoft.com/")


def preprocess4content_extractor(element: ArticleElement):
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


def process4content_extractor(tag_set, date_set, element: ArticleElement, date_):
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


def process_element(element_):
    # 将该标签内所有内容全部移除，包括子标签
    etree.strip_elements(element_, *CONTENT_EXTRACTOR_USELESS_TAGS)
    # 只移除该标签，但是保留该标签下面的子标签
    etree.strip_tags(element_, *CONTENT_EXTRACTOR_STRIP_TAGS)

    a_tag_list = element_.xpath('//a')
    for a_tag in a_tag_list:
        a_text = get_element_text_or_tail_or_attr(a_tag, 'text')
        link = get_element_text_or_tail_or_attr(a_tag, 'href')
        final_text = a_text + '<' + link + '>'
        a_tag.text = final_text
    text_list = element_.xpath('//text()')

    content_ = ';;;;'.join(text_list)
    content_ = content_.replace('\n', ';;;;').replace('\t', '').replace(u'\xa0', u' ')

    # content_ = content_.encode('utf8').decode('utf8')
    print(content_)
    return content_
