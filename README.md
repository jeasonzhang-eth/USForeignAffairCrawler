# 美国外交数据库项目
## 1. 文件夹说明
```shell
├── README.md
├── __pycache__
│   └── common.cpython-310.pyc
├── common.py
├── main.py
├── result
│   ├── biden
│   │   ├── Biden_html.txt
│   │   ├── biden_link.txt
│   │   ├── biden_output.txt
│   │   ├── biden_output_html.txt
│   │   ├── json_content.txt
│   │   ├── content.xlsx
│   │   └── url_json.txt
│   └── trump
│       ├── para.txt
│       ├── trump_link.txt
│       ├── trump_output.txt
│       ├── trump_output_html.txt
│       ├── trump_output_html1.txt
│       └── trump_output_html3.txt
└── src
    ├── __init__.py
    └── president
        ├── __init__.py
        ├── biden
        │   ├── Biden_HTML.py
        │   ├── __init__.py
        │   ├── getEntryContentBiden.py
        │   ├── main.py
        │   └── getSubPage.py
        ├── bush
        │   └── __init__.py
        ├── clinton
        │   └── __init__.py
        ├── obama
        │   └── __init__.py
        └── trump
            ├── __init__.py
            ├── getEntryContent.py
            ├── getTrumpScheduleLink.py
            └── trump_HTML.py
```
所有代码都放在src目录下
所有结果都保存在
## 2. 输出结果保存建议
每一个步骤的分步结果单独保存为bak文件，下一个步骤用只读方式打开该备份文件
```shell
    # 比如：第一步的输出结果为output1.txt，在输出完成后，将output1.txt重命名为output1.txt.bak
    1.py -o output1.txt
    cp output1.txt output1.txt.bak
    2.py -i output1.txt.bak -o output2.txt
```