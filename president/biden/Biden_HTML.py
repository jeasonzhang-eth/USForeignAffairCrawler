from utils.element_operation import get_element_text_or_tail_or_attr
from lxml.html import fromstring
from lxml import etree
from html import unescape

if __name__ == '__main__':
    output_file = open('../../../result/biden/biden_output.txt', 'w+', encoding="utf8")
    output_file_html = open('../../../result/biden/biden_output_html.txt', 'w+', encoding="utf8")
    count = 0
    for line in open('../../../result/biden/Biden_html.txt', 'r', encoding='utf8'):
        line = line.replace('\n', '')
        count += 1
        html = line.split('\t')[1]  # .replace('<br>', '\n')
        selector = fromstring(html)
        p_tag_list = selector.xpath('//p')
        output_line = ''
        for p_tag in p_tag_list:
            etree.strip_tags(p_tag, 'strong', 'u', 'b', 'span', 'em', 'script')
            all_direct_children = p_tag.getchildren()
            p_text = get_element_text_or_tail_or_attr(p_tag, 'text')
            for children in all_direct_children:
                children_text = get_element_text_or_tail_or_attr(children, 'text')
                children_tail = get_element_text_or_tail_or_attr(children, 'tail')
                if children.tag == "a":
                    link = get_element_text_or_tail_or_attr(children, 'href')
                    a_text = children_text + '<' + link + '>' + children_tail
                    p_text += a_text
                elif children.tag == "br":
                    p_text += ';;;;'
                else:
                    other_text = children_text + children_tail
                    p_text += other_text
            etree.strip_elements(p_tag, 'a', 'br')
            p_tag.text = p_text
            p_tail = get_element_text_or_tail_or_attr(p_tag, 'tail')
            if p_tag.text != '':
                output_line += p_text + p_tail + ';;;;'
            # a_tag_list = p_tag.findall('a')
            # if a_tag_list:
            #     pass
            # else:
            #     pass

            # iterator = etree.ElementTextIterator(p_tag)
            #             #
            #             # element = iterator.next()
            # p_tag.
        # soup = BeautifulSoup(html, 'lxml')
        # text = '\n'.join(selector.xpath('//p/text()'))
        # etree.dump(selector, pretty_print=True)
        # print(text)
        html_out = unescape(etree.tostring(selector).decode())
        # print(count)
        print(html_out)
        output_file_html.write(html_out + '\n')
        output_line = line.split('\t')[0] + '\t' + output_line + '\n'
        output_line = output_line.replace('\u202f', '')
        output_line = output_line.replace('\xa0', '')
        output_line = output_line.replace(';;;;;;;;;;;;', ';;;;')

        output_file.write(output_line)

    output_file.close()
    output_file_html.close()
# import re
#
#
# def filter_tags(htmlstr):
#     # 先过滤CDATA
#     re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
#     re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
#     re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
#     re_br = re.compile('<br\s*?/?>')  # 处理换行
#     re_h = re.compile('</?\w+[^>]*>')  # HTML标签
#     re_comment = re.compile('<!--[^>]*-->')  # HTML注释
#     s = re_cdata.sub('', htmlstr)  # 去掉CDATA
#     s = re_script.sub('', s)  # 去掉SCRIPT
#     s = re_style.sub('', s)  # 去掉style
#     s = re_br.sub('\n', s)  # 将br转换为换行
#     s = re_h.sub('', s)  # 去掉HTML 标签
#     s = re_comment.sub('', s)  # 去掉HTML注释
#     # 去掉多余的空行
#     blank_line = re.compile('\n+')
#     s = blank_line.sub('\n', s)
#     s = replaceCharEntity(s)  # 替换实体
#     return s

#
# def replaceCharEntity(htmlstr):
#     CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
#                      'lt': '<', '60': '<',
#                      'gt': '>', '62': '>',
#                      'amp': '&', '38': '&',
#                      'quot': '"', '34': '"', }
#
#     re_charEntity = re.compile(r'&#?(?P<name>\w+);')
#     sz = re_charEntity.search(htmlstr)
#     while sz:
#         entity = sz.group()  # entity全称，如>
#         key = sz.group('name')  # 去除&;后entity,如>为gt
#         try:
#             htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
#             sz = re_charEntity.search(htmlstr)
#         except KeyError:
#             # 以空串代替
#             htmlstr = re_charEntity.sub('', htmlstr, 1)
#             sz = re_charEntity.search(htmlstr)
#     return htmlstr
#
#
# if __name__ == '__main__':
#     s = file_json_content('index.html').read()
#     news = filter_tags(s)
#     print
#     news
