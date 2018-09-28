import sys
import pandas as pd
import components.mongo_interface as mongo_interface
from pandas.io.json import json_normalize
from bson.objectid import ObjectId

pd.options.mode.chained_assignment = None


# Utils

def get_from_path(path_string, response):
    fields = path_string.split(".")
    for field in fields:
        response = response.get(field, None)
        if response is None:
            return response
    return response

# Main functions

def get_species_plot_data(species_list, id_list):
    res = mongo_interface.get_species_plot_data(species_list, id_list)
    data = {}
    for doc in res:
        data[doc["_id"]] = doc["bin_coverage_at_1x"]
    return data

def check_run_name(name):
    return mongo_interface.check_run_name(name)

def get_run_list():
    return mongo_interface.get_run_list()
    
def get_group_list(run_name=None):
    return mongo_interface.get_group_list(run_name)

def get_species_list(run_name=None):
    return mongo_interface.get_species_list(run_name)

def filter_name(species=None, group=None, run_name=None):
    result = mongo_interface.filter({"name": 1, "sample_sheet.sample_name": 1},
                                    run_name, species, group)
    return list(result)

##NOTE SPLIT/SHORTEN THIS FUNCTION
def filter_all(species=None, group=None, run_name=None, func=None, sample_ids=None, page=None):

    if sample_ids is None:
        query_result =  mongo_interface.filter(
            {
                "name" : 1,
                "properties.species": 1,
                "sample_sheet": 1
            },
            run_name, species, group, page=page)
    else:
        query_result = mongo_interface.filter(
            {
                "name": 1,
                "properties.species": 1,
                "sample_sheet" : 1
            },
            samples=sample_ids, page=page)
    
    clean_result = {}
    sample_ids = []
    unnamed_count = 0
    for item in query_result:
        sample_ids.append(item["_id"])
        sample_sheet_name = ""
        if "name" not in item:
            if "sample_sheet" in item:
                sample_sheet_name = item["sample_sheet"]["sample_name"]
            else:
                print("No sample sheet here: ", item)
                sample_sheet_name = "UNNAMED_" + str(unnamed_count)
                unnamed_count += 1
        try:
            clean_result[str(item["_id"])] = {
                "_id": str(item["_id"]),
                "name": item.get("name", sample_sheet_name),
                "species": item.get("properties", {}).get("species", "Not classified")
            }
        except KeyError as e:
            # we'll just ignore this for now
            sys.stderr.write("Error in sample. Ignored: {}\n".format(item))
        if "sample_sheet" in item:
            for key, value in item["sample_sheet"].items():
                clean_result[str(item["_id"])]["sample_sheet." + key] = value

    component_result = mongo_interface.get_results(sample_ids)
    for item in component_result:
        item_id = str(item["sample"]["_id"])
        component = item["component"]["name"]
        if "summary" in item:
            for summary_key, summary_value in item["summary"].items():
                clean_result[item_id][component + "." +
                                      summary_key] = summary_value
        else:
            pass
            # print("Missing summary", item)
        if func is not None:
            clean_result[item_id] = func(clean_result[item_id])
    
    return pd.DataFrame.from_dict(clean_result, orient="index")

def add_sample_runs(sample_df):
    """Returns the runs each sample belongs to"""
    sample_ids = sample_df["_id"].tolist()
    sample_ids = list(map(lambda x: ObjectId(x), sample_ids))
    runs = mongo_interface.get_sample_runs(sample_ids)
    sample_runs = {}
    # Weekend challenge: turn this into a double nested dictionary comprehension
    for run in runs:
        for sample in run["samples"]:
            if sample["_id"] in sample_ids:
                s = sample_runs.get(str(sample["_id"]), [])
                s.append(run["name"])
                sample_runs[str(sample["_id"])] = s
    sample_df.loc[:, 'runs'] = sample_df["_id"].map(sample_runs)
    return sample_df

def get_read_paths(samples):
    return mongo_interface.get_read_paths(samples)

# For run_checker
def get_sample_component_status(run_name):
    return mongo_interface.get_sample_component_status(run_name)