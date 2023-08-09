# -*- encoding: utf-8 -*-
"""
@File    :   america.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/9 15:56   JeasonZhang      1.0         None
"""
from classes.factory.base import AbstractFactory
from classes.operation.biden import OperationBiden
from classes.operation.bush import OperationBush
from classes.operation.obama import OperationObama
from classes.operation.trump import OperationTrump


class AmericaFactory(AbstractFactory):
    def product_operation(self, president):
        if president == 'biden':
            return OperationBiden()
        elif president == 'trump':
            return OperationTrump()
        elif president == 'obama':
            return OperationObama()
        elif president == 'bush':
            return OperationBush()
        else:
            raise Exception
