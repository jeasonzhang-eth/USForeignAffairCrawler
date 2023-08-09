# -*- encoding: utf-8 -*-
"""
@File    :   base.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/9 15:56   JeasonZhang      1.0         None
"""
import abc


class AbstractFactory:
    @abc.abstractmethod
    def product_operation(self, president):
        pass
