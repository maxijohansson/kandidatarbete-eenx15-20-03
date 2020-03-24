import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import read_and_graph as rg


BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data_path = BASE_DIR + '\\data\\app_dir\\'
files = os.listdir(data_path)
print(files)
files_to_graph = [files[0]]
# df = rg.read_data(data_path + files[0])


app.layout = html.Div(children=[
    # html.H1(children=''),

    html.Div(
        children = [
            html.H3('Files to plot'),
            dcc.Dropdown(
                id = 'files',
                options = [
                    {'label': file, 'value': file} for file in files
                ],
                multi = True,
                value = ['asfalt1.h5'],
                style = {'width': 300}, 
            ),
        ],
        style={'width': '30%', 'float': 'left', 'display': 'inline-block'}
    ),

    html.Div([
        dcc.Graph(id = 'amplitude'),
        dcc.Graph(id = 'phase'),
    ], style={'display': 'inline-block', 'height': 400, 'width': '100%'})

])


def make_graph(x, ys, title):
    data = []
    for x,y in zip(x,ys):
        for y in y:
            data.append(
                dict(
                x = x,
                y = y,
                # color=df['2year'], 
                mode='markers',
                marker={
                    'size': 3,
                })
            )
    
    return {
        'data': data,
        'layout': dict(
            xaxis = {
                'title': 'distance',
                'tickmode': 'linear',
            },
            yaxis = {
                'title': title,
            },
            margin = {'l': 50, 'b': 40, 't': 10, 'r': 0},
            hovermode = 'closest'
        )
    }


@app.callback(
    [Output(component_id='amplitude', component_property='figure'),
    Output(component_id='phase', component_property='figure')],
    [Input(component_id='files', component_property='value')])
def update_graphs(files):
    files_to_graph = files
    dparams = [0,0]
    x = []
    y_amplitudes = []
    y_phases = []

    for i,file in enumerate(files_to_graph):
        iq = rg.read_data(data_path + file)
        amplitude, phase = rg.polar(iq)

        meta = rg.read_meta(data_path + file)
        d = round(meta['step_length_m']*100, 6)
        dparams[0] = meta['range_start_m']
        samples = len(amplitude.columns)
        x.append([dparams[0] + i*d for i in range(samples)])

        y_amplitudes.append([])
        y_amplitudes[i].append(amplitude.mean(axis='rows'))
        y_amplitudes[i].append(y_amplitudes[i][0] + amplitude.std())
        y_amplitudes[i].append(y_amplitudes[i][0] - amplitude.std())

        y_phases.append([])
        y_phases[i].append(phase.mean(axis='rows'))
        y_phases[i].append(y_phases[i][0] + phase.std())
        y_phases[i].append(y_phases[i][0] - phase.std())

    amplitude = make_graph(x, y_amplitudes, 'amplitude')
    phase = make_graph(x, y_phases, 'phase')
    
    return amplitude, phase
        

if __name__ == '__main__':
    app.run_server(debug=True)