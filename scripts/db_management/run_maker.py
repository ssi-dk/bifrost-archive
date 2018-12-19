# Removes orphans in the database: Samples with no runs, sample_components with no sample or component, components with no run.
import sys
import pymongo
from bson.objectid import ObjectId


def out(t):
    sys.stdout.write(str(t))


def get_samples(db, target_samples):
    not_found = []
    duplicate_name = []
    found = []
    invalid = []
    for sample_name in target_samples:
        sample = list(db.samples.find(
            {"name": sample_name, "sample_sheet.Comments": {"$ne": "Library fail"}}, {"name": 1, "_id": 1}))
        valid = []
        for i in range(len(sample)):
            run = db.runs.find_one({"type": "routine", "samples._id": sample[i]["_id"]})
            if run is not None:
                valid.append(sample[i])
            else:
                invalid.append(sample[i])
        
        if len(valid) == 0:
            not_found.append(sample_name)
        elif len(valid) > 1:
            duplicate_name.append(sample)
        else:
            found.append(valid[0])

    out("Total input samples: {}\n".format(len(target_samples)))

    out("Found unique samples: {}\n".format(len(found)))

    out("Not-found samples: {}\n".format(len(not_found)))
    for nf in not_found:
        out("{}\n".format(nf))

    out("Duplicate samples: {}\n".format(len(duplicate_name)))
    for dp in duplicate_name:
        out(dp)
        out("\n")

    out("Invalid samples: {}\n".format(len(invalid)))
    for iv in invalid:
        out(iv)
        out("\n")

    return found


def valid_run_name(db, run_name):
    return db.runs.find_one({"name": run_name}) is None


def create_run_dict(run_name, samples):
    return {"name": run_name, "samples": samples, "type": "custom_made"}


def main(argv):
    target_samples_path = argv[1]
    out("Locating samples...\n")

    with open("keys.txt", "r") as mongo_db_key_location_handle:
        mongodb_url = mongo_db_key_location_handle.readline().strip()

    with open(target_samples_path) as i:
        target_samples = [line.strip() for line in i]

    with pymongo.MongoClient(mongodb_url) as conn:

        db = conn.get_database()

        samples = get_samples(db, target_samples)

        resp = input("\nContinue? [y/N]: ")
        if resp == "y" or resp == "Y":
            unique = False
            run_name = ""
            while not unique:
                run_name = input("Enter new run name (has to be unique): ")
                unique = valid_run_name(db, run_name)
                if unique is False:
                    out("Run name not unique.\n")
            run = create_run_dict(run_name, samples)
            db.runs.insert(run)
            out("Finished.\n")
        else:
            out("Nothing was Done.\n")


if __name__ == "__main__":
    main(sys.argv)
