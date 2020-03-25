import os
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import read_and_graph as rg


BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data_path = BASE_DIR + '\\data\\app_dir\\'
files = os.listdir(data_path)
# files_to_graph = []

marks = {i: '{}'.format(i) for i in range(0, 2001, 100)}
marks.update({2100: 'auto'})
# df = rg.read_data(data_path + files[0])


app.layout = html.Div([
    # html.H1(children=''),
    html.Div(
        [
            html.Div(
                dcc.Dropdown(
                    id = 'files',
                    options = [
                        {'label': file, 'value': file} for file in files
                    ],
                    multi = True,
                    value = [],
                    style = {'width': 600}, 
                    persistence_type = 'memory',
                ),
                style = {'width': '48%', 'display': 'inline-block'}
            ),
            html.Div(
                [
                    html.Label('Amplitude range'),
                    dcc.Slider(
                        id = 'max_amplitude',
                        min = 0,
                        max = 2100,
                        step = 100,
                        marks = marks,
                        value = 2100,
                    ),
                ],
                style = {'width': '48%', 'display': 'inline-block'}
            )       
        ],
        style={'width': '100%'}
    ),

    html.Div([
        dcc.Graph(id = 'amplitude'),
        dcc.Graph(id = 'phase'),
    ], style={'display': 'inline-block', 'height': 400, 'width': '100%'})

])


def make_graph(x, ys, title):
    data = []
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'aqua', 'chocolate', 'slategrey']
    j = 0
    for x,y in zip(x,ys):
        # colors = [mean_color, 'darkgray', 'darkgray']
        opacities = [0.8, 0.2, 0.2]
        for i,y in enumerate(y):
            data.append(
                dict(
                x = x,
                y = y,
                opacity = opacities[i],
                mode = 'markers',
                marker = {
                    'size': 2,
                    'color': colors[j],
                })
            )
        j = j+1
    
    return {
        'data': data,
        'layout': dict(
            xaxis = {
                'title': 'distance',
                'tickmode': 'linear',
                'dtick': 0.05,
            },
            yaxis = {
                'title': title,
            },
            margin = {'l': 50, 'b': 30, 't': 10, 'r': 0},
            hovermode = 'closest'
        )
    }


def update_graphs(files_to_graph):
    xs = []
    y_amplitudes = []
    y_phases = []

    for i,file in enumerate(files_to_graph):
        iq = rg.read_data(data_path + file)
        amplitude, phase = rg.polar(iq)
        meta = rg.read_meta(data_path + file)

        d = meta['step_length_m']
        x = [meta['range_start_m'] + d*i for i in range(meta['data_length'])]
        xs.append(x)
    
        y_amplitudes.append([])
        y_amplitudes[i].append(amplitude.mean(axis='rows'))
        y_amplitudes[i].append(y_amplitudes[i][0] + amplitude.std())
        y_amplitudes[i].append(y_amplitudes[i][0] - amplitude.std())

        y_phases.append([])
        y_phases[i].append(phase.mean(axis='rows'))
        y_phases[i].append(y_phases[i][0] + phase.std())
        y_phases[i].append(y_phases[i][0] - phase.std())

    amplitude = make_graph(xs, y_amplitudes, 'amplitude')
    phase = make_graph(xs, y_phases, 'phase')
    
    return amplitude, phase


@app.callback(
    [Output(component_id='amplitude', component_property='figure'),
    Output(component_id='phase', component_property='figure')],
    [Input(component_id='files', component_property='value'),
    # Input(component_id='lock_amplitude_range', component_property='value'),
    Input(component_id='max_amplitude', component_property='value')],
    [State(component_id='amplitude', component_property='figure'),
    State(component_id='phase', component_property='figure')])
def update_data(files, max_amplitude, amplitude, phase):
    files_to_graph = files

    if max_amplitude != 2100:
        amplitude['layout']['yaxis']['range'] = [0, max_amplitude]

    if len(files_to_graph) > 0:
        amplitude, phase = update_graphs(files_to_graph)
        return amplitude, phase
    else:
        return {'data': [], 'layout': {}}, {'data': [], 'layout': {}}

if __name__ == '__main__':
    app.run_server(debug=True)