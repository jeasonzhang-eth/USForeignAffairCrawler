from src.common import Browser
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    com = Browser()
    output_file_html = open('../../../result/biden/Biden_html.txt', 'w+', encoding="utf8")
    for line in open('../../../result/biden/biden_link.txt', 'r', encoding="utf8"):
        date = line.split('\t')[0].replace('Public Schedule – ', '').replace('Public Schedule: ', '')
        print(date)
        url = line.split('\t')[1]
        print(url)
        com.open_url(url)
        result = com.browser.find_element(By.CLASS_NAME, 'entry-content')
        html = result.get_attribute('innerHTML')
        html = html.replace('\t', '').replace('\n', '').replace('&nbsp;', '').replace('<p></p>', '')
        line = date + '\t' + html + '\n'
        output_file_html.write(line)
    output_file_html.close()






