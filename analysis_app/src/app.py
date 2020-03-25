import os
import pandas as pd

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

the_rows = []

app.layout = html.Div([
    html.Div([
        dt.DataTable(
            id = 'selected_file_table',
            columns = [
                {"name": i, "id": i} for i in file_table_columns
            ],
            data = []
        )
    ]),
    dcc.Tabs(id='main_tabs', value='settings_tab', children=[
        dcc.Tab(label='Settings', value='settings_tab'),
        dcc.Tab(label='Amplitude/Phase', value='ap_tab')
    ]),
    html.Div(id='main_tab'),
    html.Div(id='hidden_div', style={'display':'none'})
])


@app.callback(
    Output('main_tab', 'children'),
    [Input('main_tabs', 'value')],
    [State('selected_file_table', 'data')])
def render_content(tab, files_dict):
    files_to_graph = [str(i['filename']) for i in files_dict]
    ids_to_graph =  [i['id'] for i in files_dict]

    if tab == 'settings_tab':
        return elements.settings_tab(ids_to_graph)

    elif tab == 'ap_tab':
        return elements.ap_graph_tab(files_to_graph)

@app.callback(
    Output('selected_file_table', 'data'),
    [Input('metadata_table', 'selected_rows')])
def update_settings(selected_rows):
    if selected_rows is None:
        the_rows = []
        return {}
    else:
        the_rows = selected_rows
        file_table = metadata.iloc[selected_rows, :]
        file_table = file_table.loc[:, file_table_columns]
        return file_table.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)


