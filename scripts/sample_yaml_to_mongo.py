# Take all the available sample.yaml files and import them into the mongodb

import pymongo
import os
from bifrostlib import datahandling
import mongo_interface


def parse_run_folder(run_directory):
    """Parse the sample.yaml files in all folders in the run directory"""

    sample_info_dict = {}
    for folder in os.listdir(run_directory):
        sample_path = os.path.join(run_directory, folder)
        if os.path.isdir(sample_path):
            try:
                sample_yaml = datahandling.load_sample(os.path.join(sample_path, "sample.yaml"))
                mongo_interface.dump_sample_info(sample_yaml)
            except FileNotFoundError:
                print("Not a sample", folder)
                # This directory is not a sample.
                continue
            # except Exception as e:
            #     print(e)

    return sample_info_dict

if __name__ == "__main__":
    print("This may not be working anymore. Please check the script and update if necessary")
    #parse_run_folder("./")
