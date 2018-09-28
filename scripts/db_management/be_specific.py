# Author: Martin B.
# So the idea is that, because of a bug in the database, the ncbi_species field 
# sometimes had an "" value, instead of a null value. When, after species detection,
# it was decided to asign the 'properties.species' field, the submitted species was "",
# which is not None, so the 'properties.species' field was set to "" instead of detected sp.
# This script goes over all the sample entries and fixes this issue.

# Removes orphans in the database: Samples with no runs, sample_components with no sample or component, components with no run.
import sys
import pymongo


def out(t):
    sys.stdout.write(t)


def get_wrong_samples(db):
    out('Searching for samples with "" as species and detected species...\n')
    wrong_samples = list(db.samples.find({
        "properties.species": "",
        "properties.provided_species": "",
        "properties.detected_species": {"$nin": ["", None]}
    }))
    # "\n".join(list(map(lambda x:str(x), wrong_samples)))
    out("Wrong samples found: {}\n".format(len(wrong_samples)))
    return wrong_samples


def update_wrong_samples(db, wrong_samples):
    count = 0
    
    for sample in wrong_samples:
        db.samples.update(
            {"_id": sample["_id"]},
            {"$set":
                {
                    "properties.provided_species": None,
                    "properties.species": sample["properties"]["detected_species"]
                }
            }
        )


def main(argv):
    with open("../../resources/keys.txt", "r") as mongo_db_key_location_handle:
        mongodb_url = mongo_db_key_location_handle.readline().strip()
    with pymongo.MongoClient(mongodb_url) as conn:

        db = conn.get_default_database()

        wrong_samples = get_wrong_samples(db)


        resp = input("\nUpdate species for all? [y/N]: ")
        if resp == "y":
            update_wrong_samples(db, wrong_samples)
            out("Done.\n")
        else:
            out("Nothing was Done.\n")


if __name__ == "__main__":
    main(sys.argv)
