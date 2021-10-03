import pandas as pd
import json
import numpy as np


def link_hh_data(population_data: str, building_data: str):
    """
    Returns population data joined to the household it belongs to.

    Parameters
    ----------
    population_data : str
        [description]
    building_data : str
        [description]
    """
    pop_data = pd.read_csv(population_data)
    pop_data["hh_index"] = pop_data["hh_index"].astype(int)

    with open(building_data) as f:
        buildings = json.load(f)

    buildings = buildings["features"]
    buildings = pd.json_normalize(buildings)
    house_holds = buildings[buildings["properties.activity"] == "households"]
    merged = pop_data.merge(
        house_holds, left_on="hh_index", right_on="properties.index", validate="m:1"
    )
    merged.drop(
        columns=["geometry.type", "properties.activity", "type", "properties.index"],
        inplace=True,
    )
    merged.rename(columns={"geometry.coordinates": "hh_coords"}, inplace=True)

    activity_locs = buildings[buildings["properties.activity"] != "households"]

    all_merged = merged.merge(
        activity_locs,
        left_on=["main_activity_id", "main_activity"],
        right_on=["properties.index", "properties.activity"],
        validate="m:1",
        how="left",
    )
    all_merged.rename(columns={"geometry.coordinates": "activity_coords"}, inplace=True) 
    

    all_merged["hh_lat"] ,all_merged["hh_long"] = zip(*all_merged.loc[:,"hh_coords"])
    
    
    all_merged_not_na = all_merged[~all_merged["activity_coords"].isna()]
    all_merged_not_na["activity_lat"] ,all_merged_not_na["activity_long"] = zip(*all_merged_not_na.loc[:,"activity_coords"])

    all_merged = all_merged.join(all_merged_not_na[["activity_lat","activity_long"]])
    
    all_merged.drop(
        columns=["geometry.type", "properties.activity", "type", "properties.index","hh_coords","activity_coords"],
        inplace=True,
    )

    
    assert len(pop_data) == len(merged) == len(all_merged), "merge failed"
    

    return all_merged


if __name__ == "__main__":
    m = link_hh_data(
        R"data\city_A\population_survey.csv",
        R"C:\Users\james.holcombe\Documents\git\personal\afod-\data\city_A\building_locations.geojson",
    )
    print(m)
