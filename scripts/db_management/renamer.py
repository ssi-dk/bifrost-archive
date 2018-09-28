# Author: Martin Basterrechea
# This small script fixes some samples in the database that 
# have no 'name' property. These samples have no reads and due to 
# a buy they end up with only a sample sheet. This program checks
# unnamed samples and copies the 'sample_sheet.sample_name' prop 
# to the 'name'
 
import sys
import pymongo


def out(t):
    sys.stdout.write(t)


def get_unnamed_samples(db):
    out('Searching for samples with "sample_sheet.name" and no "name"...\n')
    unnamed_samples = list(db.samples.find({
        "name": {"$exists": False},
        "sample_sheet.sample_name": {"$exists": True}
    }))
    # "\n".join(list(map(lambda x:str(x), unnamed_samples)))
    out("Unnamed samples found: {}\n".format(len(unnamed_samples)))
    return unnamed_samples


def update_unnamed_samples(db, unnamed_samples):
    count = 0

    for sample in unnamed_samples:
        db.samples.update(
            {"_id": sample["_id"]},
            {"$set":
                {
                    "name": sample["sample_sheet"]["sample_name"]
                }
             }
        )


def main(argv):
    with open("../../resources/keys.txt", "r") as mongo_db_key_location_handle:
        mongodb_url = mongo_db_key_location_handle.readline().strip()
    with pymongo.MongoClient(mongodb_url) as conn:

        db = conn.get_default_database()

        unnamed_samples = get_unnamed_samples(db)

        resp = input("\nFix all names? [y/N]: ")
        if resp == "y":
            update_unnamed_samples(db, unnamed_samples)
            out("Done.\n")
        else:
            out("Nothing was Done.\n")


if __name__ == "__main__":
    main(sys.argv)
