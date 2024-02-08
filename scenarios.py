#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author ：Ruoxin Xiong
@Date    ：2/4/2024 5:50 PM 
'''

# scenarios.py
import streamlit as st

# Define the ranges for each machine's parameters
param_ranges = {
    'uncoiler': {'speed': (0, 1000)},
    'welder': {'temperature': (50, 400)},
    'rollformer': {'speed': (0, 200), 'size': (0, 50)},
    'sawer': {'size': (0, 20)}
}

def setup_user_defined_scenario():
    rerun_required = False  # Flag to track if rerun is required

    num_machines = st.sidebar.number_input('Number of Machines', min_value=1, value=2)
    selected_machine_id = st.sidebar.selectbox('Select Machine ID to Configure', range(1, num_machines + 1))

    # Initialize session state for machine parameters and quality history if not already present
    if 'machine_params' not in st.session_state:
        st.session_state.machine_params = {i: [] for i in range(1, num_machines + 1)}
    if 'quality_history' not in st.session_state:
        st.session_state.quality_history = []

    # Define parameters for the selected machine (as integers)
    num_params = st.sidebar.number_input(f'Number of Parameters for Machine {selected_machine_id}', min_value=1,
                                         value=2, step=1, key=f'machine_{selected_machine_id}')
    params = []
    for p in range(num_params):
        param_min, param_max = param_ranges.get('default_param', (0, 100))
        param_label = f'Param {p + 1} for Machine {selected_machine_id} ({param_min}-{param_max})'
        param_value = st.sidebar.slider(param_label, min_value=param_min, max_value=param_max, value=(param_min + param_max) // 2, step=1, key=f'machine_{selected_machine_id}_param_{p}')
        params.append(param_value)

        current_param = f'machine_{selected_machine_id}_param_{p}'
        if current_param not in st.session_state or st.session_state[current_param] != param_value:
            st.session_state[current_param] = param_value
            rerun_required = True  # Set flag to rerun

    if rerun_required:
        st.rerun()  # Rerun the app to reflect the change immediately

    # Update parameters in session state
    st.session_state.machine_params[selected_machine_id] = params
    return num_machines, selected_machine_id


def setup_ductmate_scenario():
    rerun_required = False
    # Fixed four machines for Ductmate production line
    num_machines = 4
    machine_names = ['uncoiler', 'welder', 'rollformer', 'sawer']
    machine_parameters = {
        'uncoiler': ['speed'],
        'welder': ['temperature'],
        'rollformer': ['speed', 'size'],
        'sawer': ['size']
    }

    # Initialize session state for machine parameters if not already present
    if 'ductmate_params' not in st.session_state:
        st.session_state.ductmate_params = {name: [] for name in machine_names}

    # Define parameters for each machine (as integers)
    for machine in machine_names:
        st.markdown(f"**{machine.title()} Parameters**")
        with st.expander("Settings"):
            params = []
            for param in machine_parameters[machine]:
                param_min, param_max = param_ranges[machine].get(param, (0, 100))
                param_label = f'{param.title()}'
                param_value = st.slider(param_label, min_value=param_min, max_value=param_max,
                                                value=(param_min + param_max) // 2, step=1, key=f'{machine}_{param}')
                params.append(param_value)
            st.session_state.ductmate_params[machine] = params

            for param_index, param_value in enumerate(params):
                current_param = f'{machine}_{machine_parameters[machine][param_index]}'
                if current_param not in st.session_state or st.session_state[current_param] != param_value:
                    st.session_state[current_param] = param_value
                    rerun_required = True  # Set flag to rerun

            if rerun_required:
                st.rerun()

    return num_machines, machine_names, machine_parameters
