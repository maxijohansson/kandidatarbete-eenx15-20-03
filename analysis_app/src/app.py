import os
import pandas as pd
import time
import numpy as np

import dash
import dash_table as dt
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import data_utils as utils
import app_elements as elements

from config import *


app.layout = html.Div([
    html.Div([
        elements.selected_file_table
    ]),
    html.Div(
        dcc.Tabs(id='tabs', value='settings_tab', children=[
            dcc.Tab(label='Settings', value='settings_tab'),
            dcc.Tab(label='Amplitude/Phase', value='ap_tab'),
            dcc.Tab(label='Histograms', value='hist_tab'),
            dcc.Tab(label='Z-plane', value='z_tab')
        ]),
    ),
    dcc.Loading(
        id = "loading_main_tab", 
        children = [html.Div(id='main_tab')], 
        type = "default"
    ),
    html.Div(id='hidden_div', style={'display':'none'})
])


@app.callback(
    Output('main_tab', 'children'),
    [Input('tabs', 'value')],
    [State('selected_file_table', 'data')])
def render_tab(tab, selected_files):
    # time.sleep(1)

    files_to_graph = [row['filename'] for row in selected_files if row['filename'] != None]
    ids_to_graph =  [row['id'] for row in selected_files if row['id'] != None]

    if tab == 'settings_tab':
        return elements.settings_tab(files_to_graph)

    elif tab == 'ap_tab':
        return html.Div(elements.ap_tab(files_to_graph))

    elif tab == 'hist_tab':
        return html.Div(elements.hist_tab(files_to_graph))

    elif tab == 'z_tab':
        return html.Div(elements.z_tab(files_to_graph))


@app.callback(
    Output('selected_file_table', 'data'),
    [Input('metadata_table', 'selected_rows')])
def update_settings(selected_rows):
    if selected_rows is None:
        return {}
    else:
        file_table = []
        file_table = [{col:np.nan for col in file_table_columns} for i in range(8)]
        file_table[i] = metadata.ix[selected_rows[i], file_table_columns] for i in selected_rows
        return file_table.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)


