#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author ：Ruoxin Xiong
@Date    ：2/4/2024 3:32 PM 
'''

class ProductionLine:
    def __init__(self):
        self.machines = []

    def add_machine(self, machine):
        self.machines.append(machine)

    def process_product(self, product):
        for machine in self.machines:
            machine.process(product)
