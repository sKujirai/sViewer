import base64
import io
import re
import copy

from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from plotly.tools import mpl_to_plotly
import matplotlib.pyplot as plt
import numpy as np

from .module.vtu_reader import VtkReader
from .module.draw_mesh import DrawMesh


class MeshData:

    def __init__(self):

        # VTK data
        self.ndata = 0
        self.file_list = []
        self.ios_list = []
        self.data_dict = {}

        # Display area
        self.domain = {
            'xmin': None,
            'xmax': None,
            'ymin': None,
            'ymax': None,
            'aspect': None
        }


# Mesh data
mdata = MeshData()

# Mesh drawer
drawer = DrawMesh()

# VTK Reader
reader = VtkReader()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('mesh', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                # 'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-image-upload'),
    ],
        style={'width': '100%', 'display': 'inline-block'}
    ),
    html.Div([
        # dcc.Graph(id='matplotlib-graph'),
        html.Img(id='matplotlib-graph', src=''),
    ],
        style={'width': '70%', 'display': 'inline-block'}
    ),
    html.Div([
        html.Br(),
        html.H3('Value'),
        html.Div([
            dcc.Dropdown(
                id='dropdown-value',
            ),
        ]),
        html.Br(),
        html.H3('System'),
        html.Div([
            dcc.Dropdown(
                id='dropdown-system',
            ),
        ]),
    ],
        style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'}
    ),
    html.Div([
        dcc.Slider(
            id="slider_fig_num"
        ),
    ],
        style={'width': '100%', 'display': 'inline-block', 'margin-top': '20px'}
    ),
])


@app.callback(
    [Output('slider_fig_num', 'marks'),
     Output('slider_fig_num', 'min'),
     Output('slider_fig_num', 'max'),
     Output('dropdown-value', 'options'),
     Output('dropdown-value', 'value')],
    [Input('upload-image', 'contents')],
    [State('upload-image', 'filename')],
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        list_of_sio = []
        # Set data
        mdata.ndata = len(list_of_contents)
        for c in list_of_contents:
            _, content_string = c.split(",")
            decoded = base64.b64decode(content_string)
            list_of_sio.append(io.StringIO(decoded.decode("utf-8")))
        data_zipped = zip(list_of_sio, list_of_names)
        data_zipped = sorted(data_zipped, key=lambda s: int(re.search(r'\d+', s[1]).group()))
        mdata.ios_list, mdata.file_list = zip(*data_zipped)
        # Read first data
        reader.read(copy.copy(mdata.ios_list[0]))
        mdata.data_dict = reader.get_data_dict()
        c0_xmin = np.min(reader.Coords[0, :])
        c0_xmax = np.max(reader.Coords[0, :])
        c0_ymin = np.min(reader.Coords[1, :])
        c0_ymax = np.max(reader.Coords[1, :])
        # Read last data
        reader.read(copy.copy(mdata.ios_list[-1]))
        cn_xmin = np.min(reader.Coords[0, :])
        cn_xmax = np.max(reader.Coords[0, :])
        cn_ymin = np.min(reader.Coords[1, :])
        cn_ymax = np.max(reader.Coords[1, :])
        # Set display area
        domain = {}
        domain['xmin'] = min(c0_xmin, cn_xmin)
        domain['xmax'] = max(c0_xmax, cn_xmax)
        domain['ymin'] = min(c0_ymin, cn_ymin)
        domain['ymax'] = max(c0_ymax, cn_ymax)
        len_x = domain['xmax'] - domain['xmin']
        len_y = domain['ymax'] - domain['ymin']
        domain['xmin'] -= 0.1 * len_x
        domain['xmax'] += 0.1 * len_x
        domain['ymin'] -= 0.1 * len_y
        domain['ymax'] += 0.1 * len_y
        domain['aspect'] = (domain['ymax'] - domain['ymin']) / (domain['xmax'] - domain['xmin'])
        mdata.domain = domain
        # Set slider
        marks = {i: {'label': '{}'.format(i)} for i in range(mdata.ndata)}
        # Set dropdown to select value
        options = [{'label': lbl, 'value': lbl} for lbl in mdata.data_dict.keys()]
        value = list(mdata.data_dict.keys())[0]
        return marks, 0, mdata.ndata - 1, options, value
    else:
        return {}, 0, 0, [{'label': '', 'value': ''}], ''


@app.callback(
    [Output('dropdown-system', 'options'),
     Output('dropdown-system', 'value')],
    [Input('dropdown-value', 'value')]
)
def update_system(value):
    if value is not None and value != '':
        options = [{'label': str(i + 1), 'value': i + 1} for i in range(mdata.data_dict[value])]
        sys = 0
        return options, sys
    else:
        return [{'label': '', 'value': ''}], ''


@app.callback(
    Output('matplotlib-graph', 'src'),
    [Input('slider_fig_num', 'value'),
     Input('dropdown-value', 'value'),
     Input('dropdown-system', 'value')]
)
def update_figure(ifig, tag, sys):
    if ifig is None:
        ifig = 0
    if tag is not None and tag != '' and sys > 0:
        # Read vtu data
        reader.read(copy.copy(mdata.ios_list[ifig]))
        if tag == 'Mesh':
            val = None
        else:
            val = reader.get_value(tag, system=sys)

        # Figure
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        drawer.set_domain(ax, domain=mdata.domain)
        drawer.draw(coords=reader.Coords, connectivity=reader.Lnodes, value=val)
        # plotly_fig = mpl_to_plotly(mdata.fig)

        out_img = io.BytesIO()
        fig.savefig(out_img, format='png')
        fig.clf()
        # plt.close('all')
        out_img.seek(0)  # rewind file
        encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
        return "data:image/png;base64,{}".format(encoded)
