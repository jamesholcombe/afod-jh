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








#TODO
class ArcLayerCC():
    
    GREEN_RGB = [0, 255, 0, 40]
    RED_RGB = [240, 100, 0, 40]
    
    def __init__(self,city_folder) -> None:
        self.data = link_hh_data(join(city_folder,"population_survey.csv"),join(city_folder, "building_locations.geojson"))
        self.filters = []

   













def prepare_arc_data(
    city_folder,mapbox_token,deck_id
):

    merged_pop = link_hh_data(join(city_folder,"population_survey.csv"),join(city_folder, "building_locations.geojson"))
    data = merged_pop[~merged_pop["activity_long"].isna()]
    return data


def _build_arc_layer(city_folder,mapbox_token,deck_id,):
    """[summary]

    Parameters
    ----------
    city_folder : [type]
        [description]
    mapbox_token : [type]
        [description]
    deck_id : [type]
        [description]
    """   
    
  
    data = prepare_arc_data(city_folder,mapbox_token,deck_id)

    

    GREEN_RGB = [0, 255, 0, 40]
    RED_RGB = [240, 100, 0, 40]

    view_state = pydeck.ViewState(
    latitude= data[["hh_lat","activity_lat"]].values.mean(), longitude=data[["hh_long","activity_long"]].values.mean(), bearing=45, pitch=50, zoom=8,
)

    arc_layer = pydeck.Layer(
    "ArcLayer",
    data=data,
    get_width=5,
    get_source_position=["hh_lat", "hh_long"],
    get_target_position=["activity_lat", "activity_long"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True)
 

    r = pydeck.Deck(
        map_provider="mapbox",
        # map_style="mapbox://styles/mapbox/satellite-v9",
        layers=[
            arc_layer
        ],
         )

    data = r.to_json()
    
    
    return dash_deck.DeckGL(
            data=data, mapboxKey=mapbox_token, id=deck_id, tooltip=True
        )





def build_basic_deck(city_folder: str, deck_id: str,mapbox_token : str):
    """[summary]

    Parameters
    ----------
    city_folder : str
        [description]
    deck_id : str
        [description]
    """    

    INITIAL_VIEW_STATE = pydeck.ViewState(
    latitude=56.898760320005707,
    longitude=-4.028814858097946,
    zoom=13,
    pitch=0,
    bearing=0,
)






    with open(join(city_folder, "administrative_areas.geojson")) as f:
        ad_areas = json.load(f)

    with open(join(city_folder, "administrative_zones.geojson")) as f:
        ad_zones = json.load(f)

    with open(join(city_folder, "bus_network.json")) as f:
        bus = json.load(f)

    with open(join(city_folder, "building_locations.geojson")) as f:
        builds = json.load(f)

    with open(join(city_folder, "car_network.json")) as f:
        cars = json.load(f)

    with open(join(city_folder, "rail_network.geojson")) as f:
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
        auto_highlight=True
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
        layers=[
            ad_areas,
            ad_zones,
            cars,
            buildings,
            bus_net,
        ],
        initial_view_state=INITIAL_VIEW_STATE,
    )
    return dash_deck.DeckGL(
            data=r.to_json(), mapboxKey=mapbox_token, id=deck_id, tooltip=True
        )







