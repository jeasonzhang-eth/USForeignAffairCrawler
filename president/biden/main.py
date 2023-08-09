from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from classes.browser import Browser
import json
import requests
import jsonpath


def get_article_url(baseurl_):
    # 获取正文url
    locator = (By.CLASS_NAME, "collection-info__number")
    article_number = browser.find_element(locator).text
    print(article_number)
    file_url = open("../../../result/biden/biden_link.txt", "w+", encoding="utf8")
    try:
        url_new = baseurl_ + f'?results={article_number}&gotopage=&total_pages=1&coll_filter_year=' \
                        f'&coll_filter_month=&coll_filter_speaker=' \
                        f'&coll_filter_country=&coll_filter_release_type=&coll_filter_bureau=' \
                        f'&coll_filter_program=&coll_filter_profession='
        print(url_new)
        browser.open(url_new)
        article_link_elements = browser.find_elements((By.CLASS_NAME, "collection-result__link"))
        for article_link in article_link_elements:
            line_ = article_link.text + '\t' + article_link.get_attribute("href") + '\n'
            print(line_)
            file_url.write(line_)
    except NoSuchElementException:
        print('没有找到按钮')
    file_url.close()


def get_article_json_url():
    # 获取json数据
    file_json = open("../../../result/biden/url_json.txt", "w+", encoding="utf8")
    article_list_element = browser.find_element((By.CSS_SELECTOR, "#post-22944"))
    article_list_text = article_list_element.get_attribute("data-returned-posts")
    article_id_list = article_list_text.replace('[', '').replace(']', '').split(',')
    for article_id in article_id_list:
        url_json = 'https://www.state.gov/wp-json/wp/v2/pages/' + article_id
        file_json.write(url_json + '\n')
    file_json.close()


def get_content_from_json():
    file_json_content = open("../../../result/biden/json_content.txt", "w+", encoding="utf8")
    for json_url in open("../../../result/biden/url_json.txt", "r", encoding="utf8"):
        print(json_url)
        json_url = json_url.replace('\n', '')

        # proxies = {
        #     "http": "http://127.0.0.1:7890",
        #     "https": "http://127.0.0.1:7890",
        # }
        headers = {
            'authority': 'www.state.gov',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            # 'cookie': 'ForeseeLoyalty_MID_IJ80MItY0t=2',
            'referer': 'https://www.state.gov/public-schedule-march-23-2023/',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        response = requests.get(json_url, headers=headers,  verify=False)
        print(response.status_code)
        # if response.status_code == 400:
        url2 = response.links.get('alternate')['url']
        print(url2)
        response1 = requests.get(json_url, headers=headers)  # , proxies=proxies, verify=False)
        # if response1.status_code == 200:
        json_dict = response1.content.decode()
        print(json_dict)
        jsonobj = json.loads(json_dict)

        article_id = jsonpath.jsonpath(jsonobj, 'id')
        article_content = jsonpath.jsonpath(jsonobj, 'content.rendered')
        article_slug = jsonpath.jsonpath(jsonobj, 'slug')
        article_url = jsonpath.jsonpath(jsonobj, 'guid.rendered')
        article_author = jsonpath.jsonpath(jsonobj, 'author')

        # entry = Entry()
        line = str(article_id)[1:-1] + '\t' + str(article_author)[1:-1] + '\t' + \
            str(article_slug)[2:-2] + '\t' + str(article_url)[2:-2] + '\t' + \
            str(article_content)[2:-2] + '\t' + json_dict + '\n '
        file_json_content.write(line)
        # html = etree.HTML(str_content)  # 解析HTML
        # paragraphs = html.xpath('//p/text()')
        # print(paragraphs)
        # for p in paragraphs:
        #     print(p)
    file_json_content.close()


# 判断文件是否自身执行，如果是则，执行之后的语句
if __name__ == '__main__':
    browser = Browser()
    base_url = 'https://www.state.gov/public-schedule/'
    browser.open(base_url)
    get_article_url(base_url)
    # get_article_json_url()
    get_content_from_json()
    browser.close()
