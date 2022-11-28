from src.president.biden.main import get_article_url
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
