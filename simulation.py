#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author ：Ruoxin Xiong
@Date    ：2/4/2024 3:32 PM 
'''

from machine import Machine
from product import Product
from line import ProductionLine

class Simulation:
    def __init__(self):
        self.production_line = ProductionLine()
        self.quality_function = None

    def set_quality_function(self, quality_function):
        self.quality_function = quality_function

    def add_machine(self, parameters):
        machine = Machine(parameters)
        self.production_line.add_machine(machine)

    def run(self):
        product = Product()
        self.production_line.process_product(product)
        if self.quality_function:
            self.quality_function(product, self.production_line)
        return product.quality

# User-defined quality function example
def custom_quality_function(product, production_line):
    # Example: Product quality is the average of all machine parameter values
    total_parameters_value = sum(
        sum(machine.parameters) for machine in production_line.machines
    )
    total_parameters_count = sum(
        len(machine.parameters) for machine in production_line.machines
    )
    product.quality = total_parameters_value / total_parameters_count if total_parameters_count else 0

if __name__ == "__main__":
    # Setup and run simulation
    sim = Simulation()
    sim.set_quality_function(custom_quality_function)

    # Adding machines with parameters
    sim.add_machine([80, 90])  # Parameters for machine 1
    sim.add_machine([70, 75, 80])  # Parameters for machine 2
    # ... add more machines as needed

    product_quality = sim.run()
    print(f"The product quality is {product_quality}")
