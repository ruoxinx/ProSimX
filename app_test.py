import streamlit as st
from scenarios import setup_user_defined_scenario, setup_ductmate_scenario
from quality_checks import check_quality, adjust_ranges_based_on_material
from utils import export_simulation_data
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.image as mpimg
import time
import pandas as pd

num_machines = 4
machine_names = ['uncoiler', 'welder', 'rollformer', 'sawer']
machine_parameters = {
    'uncoiler': ['speed'],
    'welder': ['temperature'],
    'rollformer': ['speed', 'size'],
    'sawer': ['size']
}

# Set the webpage title and initialize session state variables
st.set_page_config(page_title="ProSimX", page_icon=":factory:", layout='wide')
if 'quality_history' not in st.session_state:
    st.session_state.quality_history = []
if 'machine_params' not in st.session_state:
    st.session_state.machine_params = {}
if 'ductmate_params' not in st.session_state:
    st.session_state.ductmate_params = {}
if 'production_state' not in st.session_state:
    st.session_state.production_state = 'stopped'  # Track the production state
# Initialize current_machine in session state if not already set
if 'current_machine' not in st.session_state:
    st.session_state.current_machine = 0

# Main interface for displaying the introduction
st.markdown("""
    <div style="background-color:#262730;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ProSimX: Gamified Manufacturing Production Setup Process Simulator </h1>
    </div>
    """, unsafe_allow_html=True)
st.markdown("""---""")

# Image for graph nodes
img = mpimg.imread("./media/machine.png")

# Sidebar for configuration
st.sidebar.header('Production Line Configurations')

# Dropdown for selecting the scenario
scenario = st.sidebar.selectbox('Select Scenario', ['Ductmate production line', 'User-defined scenarios'], index=0)

# Input for material properties
with st.sidebar.expander("Material Properties"):
    material_density = st.number_input('Material Density', min_value=0.0, value=1.0, step=0.01)
    material_hardness = st.number_input('Material Hardness', min_value=0.0, value=1.0, step=0.01)
    # Add more material properties as needed

# Button for exporting the simulation settings and results
if st.sidebar.button('Export Simulation Data'):
    csv_string = export_simulation_data(st.session_state.quality_history, st.session_state.machine_params,
                                        st.session_state.ductmate_params, scenario, machine_names)
    st.sidebar.download_button(
        label="Download Simulation Data",
        data=csv_string,
        file_name='simulation_data.csv',
        mime='text/csv',
    )

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Scenario Layout")

    # Networkx for visualizing the production line layout
    G = nx.DiGraph()
    G.add_nodes_from(range(1, num_machines + 1))
    G.add_edges_from([(i, i + 1) for i in range(1, num_machines)])

    # Define node positions
    pos = {i: (i - 1, 1) for i in range(1, num_machines + 1)}  # Horizontal layout

    graph_placeholder = st.empty()  # Placeholder for dynamic graph updates

    # Check for Start/Stop Production buttons before drawing the graph
    if st.button('Start Production'):
        st.session_state.production_state = 'started'
        # Perform quality checks
        final_quality_checks = {
            'bubble check': True,
            'seal': True,
            'bead location': True,
            'ease of use': True
        }

        if scenario == 'Ductmate production line':
            for machine, params in st.session_state.ductmate_params.items():
                checks = check_quality(machine, dict(zip(machine_parameters[machine], params)), material_density,
                                       material_hardness)
                # Aggregate the results for the final product quality
                for check, passed in checks.items():
                    if not passed:
                        final_quality_checks[check] = False  # Mark the check as failed if any machine fails

            # Append the final quality checks to the quality history
            st.session_state.quality_history.append(final_quality_checks)

    if st.button('Stop Production'):
        st.session_state.production_state = 'stopped'

    # Drawing the graph
    fig, ax = plt.subplots(figsize=(12, 3))
    node_color = 'red' if st.session_state.production_state == 'started' else 'green'
    nx.draw(G, pos, with_labels=False, node_color=node_color, node_size=2500, edge_color='gray', font_size=10,
            font_weight='bold')

    # Annotate nodes with machine names and integer parameters
    for node, (x, y) in pos.items():
        if scenario == 'User-defined scenarios':
            machine_name = f'Machine {node}'
            params = st.session_state.machine_params.get(node, [])
        else:
            machine_name = machine_names[node - 1].title()
            params = st.session_state.ductmate_params.get(machine_name.lower(), [])

        # Convert parameters to integers and then to a formatted string
        formatted_params = ', '.join(str(int(p)) for p in params)
        ax.annotate(f'{machine_name}: [{formatted_params}]', xy=(x, y), xytext=(0, 10),
                    textcoords='offset points', ha='center', va='bottom')

    # Add legend for node colors
    red_patch = plt.Line2D([0], [0], marker='o', color='w', label='In Production', markersize=8, markerfacecolor='red')
    green_patch = plt.Line2D([0], [0], marker='o', color='w', label='Available', markersize=8, markerfacecolor='green')
    ax.legend(handles=[red_patch, green_patch], fontsize=8, loc='upper center')

    st.pyplot(fig)

    if st.button('Quality Check'):
        # Display quality check results in a table below the figure
        if 'quality_history' in st.session_state and st.session_state.quality_history:
            latest_quality_checks = st.session_state.quality_history[-1]
            # Convert quality check results to 'Pass'/'Fail' and create DataFrame
            formatted_results = {'Check': [], 'Result': []}
            for check, passed in latest_quality_checks.items():
                formatted_results['Check'].append(check.title())
                formatted_results['Result'].append("Pass" if passed else "Fail")
            df_quality_checks = pd.DataFrame(formatted_results)
            # Display the table without the index
            st.table(df_quality_checks.set_index('Check'))

with col2:
    st.markdown("### Process Control Panel")
    if st.session_state.production_state == 'stopped':
        # Scenario-specific setup
        if scenario == 'User-defined scenarios':
            num_machines, selected_machine_id = setup_user_defined_scenario()
        elif scenario == 'Ductmate production line':
            num_machines, machine_names, machine_parameters = setup_ductmate_scenario()
    else:
        st.warning("Production is running. Stop production to adjust process control settings.")