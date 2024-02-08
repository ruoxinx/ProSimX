#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author ：Ruoxin Xiong
@Date    ：2/4/2024 4:11 PM 
'''

import pandas as pd
import plotly.express as px

def plot_quality_history(quality_history):
    if quality_history:
        df = pd.DataFrame({
            'Simulation Run': range(1, len(quality_history) + 1),
            'Quality': quality_history
        })
        fig = px.line(df, x='Simulation Run', y='Quality', title='Quality Over Time')
        return fig
    else:
        raise ValueError("No quality history to plot. Run some simulations!")
