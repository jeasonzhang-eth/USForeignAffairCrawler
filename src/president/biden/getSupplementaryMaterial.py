# -*- encoding: utf-8 -*-
'''
@File    :   getSupplementaryMaterial.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2021
 
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/11/24 0:05   JeasonZhang      1.0         None
'''
import pandas as pd

if __name__ == '__main__':
    biden_df = pd.read_csv('../../../result/biden/biden_test.csv')
    link_series = biden_df['Links']
    content_html = []
    for link in link_series:
        link = link.replace('<', '').replace('>', '')
        if link not in ['None', '']:
            # print(link)
            content_html.append(link)
        else:
            content_html.append('')
    se = set(content_html)
    content_html = list(se)
    content_html.sort()

    print(';;;;'.join(content_html))
    # print(biden_df)
