# -*- encoding: utf-8 -*-
"""
@File    :   browser.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/7 15:51   JeasonZhang      1.0         None
"""
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class Browser(object):
    """
    selenium框架的主要类
    """
    original_window = None

    def __init__(self, browser='chrome'):
        """
        运行初始化方法默认chrome，当然，你也可以传入一个其他浏览器名称，
        """
        # 浏览器最大化
        if browser == "firefox" or browser == "ff":
            self.driver = webdriver.Firefox()
        elif browser == "chrome":
            options = Options()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--user-data-dir="+r"C:\Users\jie\AppData\Local\Google\Chrome\User Data\Default")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()
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
        self.driver.maximize_window()

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

    def find_elements(self, locator, timeout=60):
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
    driver = Browser("chrome")
    # 检查是否处理反爬
    driver.open("https://bot.sannysoft.com/")