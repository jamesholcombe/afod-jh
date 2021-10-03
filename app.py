import os
import dash

# from dash_core_components.Dropdown import Dropdown
from dash import html, dcc
import pandas as pd
import pydeck
import json
import dash_deck
from os.path import join
import os
from pydeck.bindings import view_state
from deck_helpers import link_hh_data
from layers import build_arc_layer


mapbox_api_token = "pk.eyJ1IjoiamFtZXNob2xjbyIsImEiOiJja3JhaWpkOXcwNjdpMnRuaWRwdDF1bGFnIn0.rgnszUE9Qu79gIzQJ_EdxQ"


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__)



app.layout = html.Div(
    build_arc_layer(join(os.getcwd(),"data\city_A"),mapbox_api_token,"test")
)



if __name__ == "__main__":
    app.run_server(debug=True)
