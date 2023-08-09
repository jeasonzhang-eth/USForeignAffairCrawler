from classes.browser import Browser
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    output_file = open('../../../result/trump/trump_link.txt', 'w+', encoding="utf8")
    com = Browser()
    for i in range(1, 114):
        if i == 1:
            url = 'https://2017-2021.state.gov/public-schedule/index.html'
        else:
            url = 'https://2017-2021.state.gov/public-schedule/page/' + str(i) + '/index.html'
        print(url)
        com.open_url(url)
        results = com.browser.find_elements(By.CLASS_NAME, 'collection-result__link')
        for result in results:
            line = result.text + '\t' + result.get_attribute("href") + '\n'
            output_file.write(line)
            print(line)
    output_file.close()
