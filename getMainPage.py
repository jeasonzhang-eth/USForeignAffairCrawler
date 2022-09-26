import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from selenium.webdriver.chrome.options import Options


class Common(object):
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


# 判断文件是否自身执行，如果是则，执行之后的语句
if __name__ == '__main__':
    com = Common()
    url = 'https://www.state.gov/public-schedule/'
    com.open_url(url)
    article_number = com.browser.find_element(By.CLASS_NAME, "collection-info__number")
    print(article_number.text)
    # com.browser.save_screenshot('save.png')
    # select_element = com.browser.find_element(By.CSS_SELECTOR, '#pagination > div:nth-child(1) > select')
    # select_object = Select(select_element)
    # select_object.select_by_value('30')
    try:
        url_new = url + f'?results={article_number.text}&gotopage=&total_pages=1&coll_filter_year=' \
                        f'&coll_filter_month=&coll_filter_speaker=' \
                        f'&coll_filter_country=&coll_filter_release_type=&coll_filter_bureau=' \
                        f'&coll_filter_program=&coll_filter_profession='
        print(url_new)
        com.open_url(url_new)
        articles = com.browser.find_elements(By.CLASS_NAME, "collection-result__link")
        file = open("urls.txt", "w+", encoding="utf8")
        for article in articles:
            url = article.get_attribute('href')
            print(url)
            file.write(url)
            file.write("\n")
        # btn = com.browser.find_element(By.CSS_SELECTOR,
        #                                "#post-22944 > div > div.collection-list > div > div > a.next.page-numbers")
        # btn.click()
        file.close()
    except NoSuchElementException:
        print('没有找到按钮')

    time.sleep(300)
    com.close_driver()
