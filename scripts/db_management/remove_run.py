# Removes orphans in the database: Samples with no runs, sample_components with no sample or component, components with no run.
import sys
import pymongo
from bson.objectid import ObjectId


def out(t):
    sys.stdout.write(t)


def get_run_id(db, target_run):
    run = db.runs.find_one({"_id": ObjectId(target_run)})
    if run is None:
        out("Run not found.")
        exit()
    out("Run with id {} found.\n".format(str(run["_id"])))
    return run["_id"], list(map(lambda x: x["_id"], run["samples"]))


def get_single_parent_samples(db, run_id, sample_ids):
    runs = db.runs.find(
        {"samples._id": {"$in": sample_ids}, "_id": {"$ne": run_id}})
    sample_ids_set = set(sample_ids)
    samples_in_other_runs_set = set()
    for run in runs:
        samples_in_other_runs_set |= set(
            list(map(lambda x: x["_id"], run["samples"])))

    return (sample_ids_set - samples_in_other_runs_set)


def get_single_parent_components(db, sample_ids):
    samples = db.samples.find({"_id": {"$in": sample_ids}})
    component_ids_set = set()
    for sample in samples:
        if "components" in sample:
            component_ids_set |= set(
                list(map(lambda x: x["_id"], sample["components"])))

    other_samples = db.samples.find({
        "components._id": {"$in": list(component_ids_set)},
        "_id": {"$nin": sample_ids}
    })
    components_in_other_runs_set = set()

    for sample in other_samples:
        components_in_other_runs_set |= set(
            list(map(lambda x: x["_id"], sample["components"])))
    return (component_ids_set - components_in_other_runs_set), component_ids_set


def get_sample_components(db, sample_ids, component_ids_set):
    s_c = db.sample_components.find({
        "sample._id": {"$in": sample_ids},
        "component._id": {"$in": list(component_ids_set)}
    })
    return list(map(lambda x: x["_id"], s_c))


def delete_all(db,
               run_id,
               single_parent_samples_set,
               single_parent_components_set,
               sample_components):
    out("Removing sample_components...\n")
    db.sample_components.delete_many({"_id": {"$in": sample_components}})
    out("Done.\n")
    out("Removing components...\n")
    db.components.delete_many(
        {"_id": {"$in": list(single_parent_components_set)}})
    out("Done.\n")
    out("Removing samples...\n")
    db.samples.delete_many({"_id": {"$in": list(single_parent_samples_set)}})
    out("Done.\n")
    out("Removing run...\n")
    db.runs.delete_one({"_id": ObjectId(run_id)})
    out("Done.\n")


def main(argv):
    target_run = argv[1]
    out("Locating run {}...\n".format(target_run))
    with open("../../resources/keys.txt", "r") as mongo_db_key_location_handle:
        mongodb_url = mongo_db_key_location_handle.readline().strip()
    with pymongo.MongoClient(mongodb_url) as conn:

        db = conn.get_database()

        run_id, sample_ids = get_run_id(db, target_run)

        single_parent_samples_set = get_single_parent_samples(
            db, run_id, sample_ids)

        single_parent_components_set, component_ids_set = get_single_parent_components(
            db, sample_ids)

        sample_components = get_sample_components(
            db, sample_ids, component_ids_set)

        out("Single parent samples ({}):\n{}\n".format(
            len(single_parent_samples_set),
            "\n".join(map(str, single_parent_samples_set))
        ))
        out("Single parent components ({}):\n{}\n".format(
            len(single_parent_components_set),
            "\n".join(map(str, single_parent_components_set))
        ))
        out("Sample_components ({}):\n{}\n".format(
            len(sample_components),
            "\n".join(map(str, sample_components))
        ))

        resp = input("\nDelete all? [y/N]: ")
        if resp == "y" or resp == "Y":
            delete_all(db,
                       run_id,
                       single_parent_samples_set,
                       single_parent_components_set,
                       sample_components)
            out("Finished.\n")
        else:
            out("Nothing was Done.\n")


if __name__ == "__main__":
    main(sys.argv)
