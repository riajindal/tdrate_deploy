"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import socket

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("TD Rate Dashboard", className="display-5"),
        html.Hr(),
        html.P(
            "Analysis of interest rates based on tenure and revenue", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Tenure Comparison - Slabs", href="/", active="exact"),
                dbc.NavLink("Tenure Comparison - Daily", href="/page-2", active="exact"),
                dbc.NavLink("Revenue Comparison", href="/page-3", active="exact"),
                dbc.NavLink("Historical Comparison", href="/page-4", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(children=dash.page_container, style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


def find_available_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))  # Bind to a random available port
    _, port = sock.getsockname()
    sock.close()
    return port


# Usage
port = find_available_port()
print(f"Available port: {port}")

# Use the port variable in your Dash app configuration
app.run_server(debug=False, port=port)
