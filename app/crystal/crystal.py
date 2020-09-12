from django_plotly_dash import DjangoDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import os

from .module.fcc import FCC
from .module.bcc import BCC
from .module.hcp import HCP


def get_go_axis():

    length = 1.

    go_x_axis = go.Scatter3d(
        x=[0., length],
        y=[0., 0.],
        z=[0., 0.],
        line=dict(width=6, color='red'),
        name='X-axis'
    )

    go_y_axis = go.Scatter3d(
        x=[0., 0.],
        y=[0., length],
        z=[0., 0.],
        line=dict(width=6, color='blue'),
        name='Y-axis'
    )

    go_z_axis = go.Scatter3d(
        x=[0., 0.],
        y=[0., 0.],
        z=[0., length],
        line=dict(width=6, color='green'),
        name='Z-axis'
    )

    return [go_x_axis, go_y_axis, go_z_axis]


fcc = FCC()
bcc = BCC()
hcp = HCP()

app = DjangoDash('crystal')

app.layout = html.Div([
    html.H1('Lattice Viewer'),
    html.Div([
        dcc.Graph(
            id='graph_crystal'
        )],
        # style={'width': '70%', 'minWidth': 500, 'display': 'inline-block'}
        style={'width': '70%', 'display': 'inline-block'}
    ),
    html.Div([
        html.Br(),
        html.Div([
            html.H3('Rotation angle'),
            html.Div([
                html.Label('theta'),
                dcc.Dropdown(
                    id='angle-the',
                    options=[{'label': i, 'value': i} for i in range(-180, 181)],
                    value=0,
                )],
                style={'width': '33%', 'display': 'inline-block'}
            ),
            html.Div([
                html.Label('phi'),
                dcc.Dropdown(
                    id='angle-phi',
                    options=[{'label': i, 'value': i} for i in range(-180, 181)],
                    value=0,
                )],
                style={'width': '33%', 'display': 'inline-block'}
            ),
            html.Div([
                html.Label('psi'),
                dcc.Dropdown(
                    id='angle-psi',
                    options=[{'label': i, 'value': i} for i in range(-180, 181)],
                    value=0,
                )],
                style={'width': '33%', 'display': 'inline-block'}
            ),
        ],
            style={'width': 'auto', 'display': 'inline-block', 'vertical-align': 'top'}
        ),
        html.Br(),
        html.H3('Select crystal'),
        dcc.Dropdown(
            id='dropdown_crystal',
            options=[{'label': cry, 'value': cry} for cry in ['FCC', 'BCC', 'HCP']],
            value='FCC',
            multi=True
        ),
        html.Br(),
        html.H3('Rotation matrix'),
        dcc.Dropdown(
            id='dropdown_rotation',
            options=[{'label': rot, 'value': rot} for rot in ['Euler-XYZ', 'Bunge']],
            value='Euler-XYZ',
        ),
        html.Br(),
        html.H3('Axes'),
        dcc.RadioItems(
            id='checkbox_show_axis',
            options=[
                {'label': 'Show axes', 'value': 'show'},
                {'label': 'hide axes', 'value': 'hide'}
            ],
            value='show'
        )
    ],
        style={'width': 'auto', 'display': 'inline-block', 'vertical-align': 'top'}
    ),
])


@app.callback(
    Output('graph_crystal', 'figure'),
    [Input('dropdown_crystal', 'value'),
     Input('angle-the', 'value'),
     Input('angle-phi', 'value'),
     Input('angle-psi', 'value'),
     Input('dropdown_rotation', 'value'),
     Input('checkbox_show_axis', 'value')]
)
def update_crystal(cry, the, phi, psi, rot_type, show_axis):
    data = []
    if show_axis == 'show':
        data = data + get_go_axis()
    if 'FCC' in cry:
        fcc.update([the, phi, psi], rot_type)
        data = data + fcc.data_go
    if 'BCC' in cry:
        bcc.update([the, phi, psi], rot_type)
        data = data + bcc.data_go
    if 'HCP' in cry:
        hcp.update([the, phi, psi], rot_type)
        data = data + hcp.data_go
    fig = {
        'data': data,
        'layout': {
            'height': 750,
            # 'minHeight': 700,
        }
    }
    return fig
