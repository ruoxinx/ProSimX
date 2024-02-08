#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author ：Ruoxin Xiong
@Date    ：2/4/2024 9:21 PM 
'''
import io
import pandas as pd


def export_simulation_data(quality_history, machine_params, ductmate_params, scenario, machine_names):
    # Check if the data is present
    if not quality_history:
        print("Quality history is empty.")  # You can change print to st.write if you want it to display in the app
        return ""

    # Create a list of dictionaries, each containing the data for one simulation run
    data_for_export = []
    for i, quality_checks in enumerate(quality_history, 1):
        if scenario == 'User-defined scenarios':
            params = machine_params.get(i, {})
            if not params:
                print(f"No parameters found for machine {i} in user-defined scenarios.")
        else:
            params = {machine: ductmate_params.get(machine, []) for machine in machine_names}
            if not any(params.values()):
                print(f"No parameters found for machines in Ductmate production line.")

        # Formatting the quality checks data
        formatted_quality_checks = {check: 'Pass' if passed else 'Fail' for check, passed in
                                    quality_checks.items()}

        data_for_export.append({
            'Simulation Run': i,
            'Machine Parameters': str(params),
            'Quality Checks': str(formatted_quality_checks)
        })

    if not data_for_export:
        print("No data to export.")
        return ""

    # Create a DataFrame with the simulation settings and results
    df_export = pd.DataFrame(data_for_export)

    # Convert DataFrame to CSV
    csv_buffer = io.StringIO()
    df_export.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    csv_string = csv_buffer.getvalue()
    return csv_string
