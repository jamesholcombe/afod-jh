import dash
# from dash_core_components.Dropdown import Dropdown
from dash import html ,dcc
import pandas as pd
import pydeck
import json
import dash_deck


INITIAL_VIEW_STATE = pydeck.ViewState(
    latitude=56.898760320005707, longitude=-4.028814858097946, zoom=9,  pitch=0, bearing=0
)

with open(R"data\city_A\administrative_areas.geojson") as f:
    ad_areas = json.load(f)

with open(R"data\city_A\administrative_zones.geojson") as f:
    ad_zones = json.load(f)

with open(R"data\city_A\bus_network.json") as f:
    bus = json.load(f)

with open(R"data\city_A\building_locations.geojson") as f:
    builds = json.load(f)

with open(R"data\city_A\car_network.json") as f:
    cars = json.load(f)








ad_areas = pydeck.Layer("GeoJsonLayer", ad_areas, get_fill_color=[155, 165, 0])
ad_zones = pydeck.Layer("GeoJsonLayer", ad_zones, get_fill_color=[155, 165, 100])
bus_net = pydeck.Layer("GeoJsonLayer", bus, get_radius = 200,get_fill_color=[255, 165, 0],get_line_color=[255, 255, 255])
buildings = pydeck.Layer("GeoJsonLayer", builds, get_radius = 7,get_fill_color=[255, 165, 0],get_line_color=[255, 255, 255])
cars =  pydeck.Layer("GeoJsonLayer", cars, get_radius = 200,get_fill_color=[0, 0, 0],get_line_color=[0, 0, 0])



r = pydeck.Deck(
    map_provider="mapbox",
    map_style="mapbox://styles/mapbox/satellite-v9",
    layers=[cars,buildings,bus_net],
    initial_view_state=INITIAL_VIEW_STATE,
    )
mapbox_api_token = "pk.eyJ1IjoiamFtZXNob2xjbyIsImEiOiJja3JhaWpkOXcwNjdpMnRuaWRwdDF1bGFnIn0.rgnszUE9Qu79gIzQJ_EdxQ"


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash_app.server

dash_app.layout = html.Div(


    dash_deck.DeckGL(
                                data=r.to_json(),
                                mapboxKey=mapbox_api_token,
                                id="deck-gl",  
                            ),


)


if __name__ == "__main__":
    dash_app.run_server(debug=True)










