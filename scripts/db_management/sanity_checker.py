# Removes orphans in the database: Samples with no runs, sample_components with no sample or component, components with no run.
import sys
import pymongo

def out(t):
    sys.stdout.write(t)

def get_orphan_samples(db):
    out("Searching for orphaned samples...\n")
    all_samples = db.samples.find({})
    sample_ids = set()
    for sample in all_samples:
        sample_ids.add(sample["_id"])
    
    all_runs = db.runs.find({}, {"samples._id": 1})
    samples_in_runs = set()
    for run in all_runs:
        for sample in run["samples"]:
            samples_in_runs.add(sample["_id"])
    orphan_samples = sample_ids - samples_in_runs
    # "\n".join(list(map(lambda x:str(x), orphan_samples)))
    out("Total samples found: {}\n".format(len(sample_ids)))
    out("Samples in runs found: {}\n".format(len(samples_in_runs)))
    out("Orphaned samples found: {}\n".format(len(orphan_samples)))
    # out("\n".join(map(lambda x:str(x), orphan_samples)) + "\n")
    return list(orphan_samples), list(samples_in_runs)


def get_orphan_components(db):
    out("Searching for orphaned components...\n")
    all_components = db.components.find({})
    component_ids = set()
    for component in all_components:
        component_ids.add(component["_id"])

    all_runs = db.runs.find({}, {"components._id": 1})
    components_in_runs = set()
    for run in all_runs:
        for component in run["components"]:
            components_in_runs.add(component["_id"])
    orphan_components = component_ids - components_in_runs
    # "\n".join(list(map(lambda x:str(x), orphan_components)))
    out("Total components found: {}\n".format(len(component_ids)))
    out("components in runs found: {}\n".format(len(components_in_runs)))
    out("Orphaned components found: {}\n".format(len(orphan_components)))
    return list(orphan_components), list(components_in_runs)


def get_orphan_sample_components(db, good_samples, good_components):
    out("Searching for orphaned sample_components...\n")
    orphan_scs = db.sample_components.find({
        "$or": [
            {"sample._id": {"$nin": good_samples}},
            {"component._id": {"$nin": good_components}}
        ]
    })

    out("Orphaned sample_compnents found: {}\n".format(len(list(orphan_scs))))
    return list(orphan_scs)


def delete_all(db, orphan_samples, orphan_components, orphan_sc):
    db.samples.delete_many({"_id": {"$in": orphan_samples}})
    db.components.delete_many({"_id": {"$in": orphan_components}})
    db.sample_components.delete_many({"_id": {"$in": orphan_sc}})

def main(argv):
    with open("../../resources/keys.txt", "r") as mongo_db_key_location_handle:
        mongodb_url = mongo_db_key_location_handle.readline().strip()
    with pymongo.MongoClient(mongodb_url) as conn:

        db = conn.get_default_database()

        orphan_samples, good_samples = get_orphan_samples(db)

        orphan_components, good_components = get_orphan_components(db)

        orphan_sc = get_orphan_sample_components(
            db, good_samples, good_components)
        
        resp = input("\nDelete all? [y/N]: ")
        if resp == "y":
            delete_all(db, orphan_samples, orphan_components, orphan_sc)
            out("Done.\n")
        else:
            out("Nothing was Done.\n")

if __name__ == "__main__":
    main(sys.argv)
