#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author ：Ruoxin Xiong
@Date    ：2/4/2024 9:21 PM 
'''

# quality_checks.py

# Define the acceptable ranges for each machine's parameters
acceptable_ranges = {
    'uncoiler': {'speed': (50, 100)},  # Example ranges, adjust as needed
    'welder': {'temperature': (200, 300)},
    'rollformer': {'speed': (60, 120), 'size': (10, 20)},
    'sawer': {'size': (5, 10)}
}

def check_quality(machine_name, parameters, material_density, material_hardness):
    quality_checks = {
        'bubble check': True,
        'seal': True,
        'bead location': True,
        'ease of use': True
    }
    # Adjust the acceptable ranges based on material properties
    adjusted_acceptable_ranges = adjust_ranges_based_on_material(acceptable_ranges, material_density, material_hardness)

    # Check if each parameter is within the acceptable range
    for param, value in parameters.items():
        if param in adjusted_acceptable_ranges[machine_name]:
            min_val, max_val = adjusted_acceptable_ranges[machine_name][param]
            if not (min_val <= value <= max_val):
                # If any parameter is out of range, mark all checks as failed
                quality_checks = {k: False for k in quality_checks}
                break
    return quality_checks

def adjust_ranges_based_on_material(acceptable_ranges, density, hardness):
    # Logic to adjust ranges based on material properties
    # For simplicity, this is a placeholder, implement your own logic
    adjusted_ranges = {machine: {param: (min_val * density, max_val * hardness)
                                 for param, (min_val, max_val) in params.items()}
                       for machine, params in acceptable_ranges.items()}
    return adjusted_ranges
