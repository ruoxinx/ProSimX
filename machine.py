#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author ：Ruoxin Xiong
@Date    ：2/4/2024 3:30 PM 
'''
class Machine:
    def __init__(self, parameters):
        self.parameters = parameters

    def process(self, product):
        # For demonstration, just add the sum of parameters to product's quality
        product.quality += sum(self.parameters)
