import pandas as pd
import json



def link_hh_data(population_data : str,building_data : str ):
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
    merged = pop_data.merge(house_holds,left_on="hh_index",right_on="properties.index",validate="m:1")
    return merged.iloc[:,1:]
    

    

    



if __name__ == "__main__":
    m = link_hh_data(
        R"data\city_A\population_survey.csv",
       R"C:\Users\james.holcombe\Documents\git\personal\afod-\data\city_A\building_locations.geojson"
    )
    print(m)








