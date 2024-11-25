import logging

import dash
import dash_bootstrap_components as dbc

from args import ArgParser
from callbacks import add_callbacks
from layout import layout

logger = logging.getLogger(__name__)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
server = app.server
app.title = "Hybrid Image Playground"
app.layout = layout
add_callbacks(app)

if __name__ == "__main__":
    args = ArgParser()

    args.parser.parse_args()

    app.run_server(debug=True, port=8300)
