# Author: Martin Basterrechea
# Find samples for which a specific component has not been run

import sys
import pymongo


def out(t):
    sys.stdout.write(t)


def get_samples_no_component(db, comp_name):
    #out('Searching for samples with "sample_sheet.name" and no "name"...\n')
    runs = list(db.runs.find({
        "components": {"$not": {"$elemMatch": {"name": comp_name}}},
        "type": "routine"
    }, {"samples", "name"}))
    samples = ["name\t_id\trun"]
    for run in runs:
        run_samples = run["samples"]
        samples = samples + \
            list(map(lambda x: "{}\t{}\t{}".format(
                x["name"], x["_id"], run["name"]), run_samples))

    #out("Samples found with no {} component: {}\n".format(comp_name, len(unnamed_samples)))
    
    # Print all runs
    out("\n".join(list(map(lambda x:x["name"], runs))))

    # Print all samples
    # out("\n".join(samples) + "\n")
    #return unnamed_samples



def main(argv):
    with open("../../resources/keys.txt", "r") as mongo_db_key_location_handle:
        mongodb_url = mongo_db_key_location_handle.readline().strip()
    with pymongo.MongoClient(mongodb_url) as conn:

        db = conn.get_database()

        component_name = argv[1]

        get_samples_no_component(db, component_name)

        # resp = input("\nFix all names? [y/N]: ")
        # if resp == "y":
        #     update_unnamed_samples(db, unnamed_samples)
        #     out("Done.\n")
        # else:
        #     out("Nothing was Done.\n")


if __name__ == "__main__":
    main(sys.argv)
