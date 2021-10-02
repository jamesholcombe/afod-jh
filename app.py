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


INITIAL_VIEW_STATE = pydeck.ViewState(
    latitude=56.898760320005707,
    longitude=-4.028814858097946,
    zoom=13,
    pitch=0,
    bearing=0,
)


def build_deck(city_folder : str,deck_id : str):

    with open(join(city_folder,"city_A\administrative_areas.geojson")) as f:
        ad_areas = json.load(f)

    with open(join(city_folder,"city_A\administrative_zones.geojson")) as f:
        ad_zones = json.load(f)

    with open(join(city_folder,"city_A\bus_network.json")) as f:
        bus = json.load(f)

    with open(join(city_folder,"city_A\building_locations.geojson")) as f:
        builds = json.load(f)

    with open(join(city_folder,"city_A\car_network.json")) as f:
        cars = json.load(f)

    with open(join(city_folder,"city_A\rail_network.geojson")) as f:
        rail = json.load(f)

    ad_areas = pydeck.Layer("GeoJsonLayer", ad_areas, get_fill_color=[155, 165, 0])
    ad_zones = pydeck.Layer("GeoJsonLayer", ad_zones, get_fill_color=[155, 165, 100])
    bus_net = pydeck.Layer(
        "GeoJsonLayer",
        bus,
        get_line_width=2,
        get_fill_color=[255, 165, 0],
        get_line_color=[255, 255, 255],
    )
    buildings = pydeck.Layer(
        "GeoJsonLayer",
        builds,
        get_radius=4,
        get_fill_color=[255, 165, 0],
        pickable=True,
        auto_highlight = True
        # get_line_color=[255, 255, 255],
    )
    cars = pydeck.Layer(
        "GeoJsonLayer",
        cars,
        get_line_width=5,
        get_fill_color=[58, 50, 161],
        get_line_color=[58, 50, 161],
    )
    rail = pydeck.Layer(
        "GeoJsonLayer",
        rail,
        get_line_width=0,
        get_fill_color=[255, 165, 0],
        get_line_color=[255, 255, 255],
    )

    r = pydeck.Deck(
        map_provider="mapbox",
        # map_style="mapbox://styles/mapbox/satellite-v9",
        layers=[ad_areas,ad_zones, cars, buildings, bus_net,],
        initial_view_state=INITIAL_VIEW_STATE,
    )
    return dash_deck.DeckGL(
        data=r.to_json(),
        mapboxKey=mapbox_api_token,
        id=deck_id,
        tooltip=True
    ),






mapbox_api_token = "pk.eyJ1IjoiamFtZXNob2xjbyIsImEiOiJja3JhaWpkOXcwNjdpMnRuaWRwdDF1bGFnIn0.rgnszUE9Qu79gIzQJ_EdxQ"


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash_app.server



if __name__ == "__main__":
    dash_app.run_server(debug=True)
