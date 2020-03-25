import dash
import dash_table as dt
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import data_utils as utils

from config import *

def settings_tab(files_to_graph):
	return(
		html.Div(
            [
            html.Div(
                dt.DataTable(
                    id='metadata_table',
                    columns=[
                        {"name": i, "id": i, "deletable": False, "selectable": True} for i in metadata.columns
                    ],
                    data=metadata.to_dict('records'),
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    selected_rows=files_to_graph,
                    page_action="native",
                    page_current= 0,
                )
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
    	)
	)


def ap_graph_tab(files_to_graph):
    amplitude, phase = ap_graph(files_to_graph)

    return(
    	html.Div([
            dcc.Graph(id = 'amplitude', figure=amplitude),
            dcc.Graph(id = 'phase', figure=phase),
        ], style={'display': 'inline-block', 'height': 400, 'width': '100%'})
    )


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
        iq = utils.read_data(data_path + file)
        amplitude, phase = utils.polar(iq)
        meta = utils.read_meta(data_path + file)

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


def ap_graph(files_to_graph):
    if len(files_to_graph) > 0:
        return update_graphs(files_to_graph)
    else:
        return {'data': [], 'layout': {}}, {'data': [], 'layout': {}}

	