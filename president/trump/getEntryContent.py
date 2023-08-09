from classes.browser import Browser
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    com = Browser().browser

    output_file_html = open('../../../result/trump/trump_output_html1.txt', 'w+', encoding="utf8")
    for line in open('../../../result/trump/trump_link.txt', 'r', encoding="utf8"):
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
        output_file_html.flush()
    output_file_html.close()






