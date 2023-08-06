# 美国外交数据库项目
## 1. 文件夹说明
```shell

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

## 3. 最终输出文件定义

| 列名            | 含义                   |
| --------------- | ---------------------- |
| Date            | 日期                   |
| President       | 总统名称               |
| article_link    | 该日期下发布的文章链接 |
| article_html    | 该日期下发布的文章的   |
| article_content | 该日期下发布的文章内容 |

