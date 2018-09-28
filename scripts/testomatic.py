import os
import re
import datahandling
import operator

MINSPECIES = 0.95

CONTIGMAX = 1500

AVGCOVERAGE_FAIL = 25
AVGCOVERAGE_WARN = 50

NUMREADS_FAIL = 10000
NUMREADS_WARN = 100000

def generate_summary(results):
    summary = {}
    for result in results:
        summary[result["name"]] = result["status"] + ":" + result["reason"]
    return summary

def script__test_testomatic(qcquickie_yaml, assemblatron_yaml, whats_my_species_yaml, sample, sample_component):

    qcquickie = datahandling.load_sample_component(qcquickie_yaml)
    whats_my_species = datahandling.load_sample_component(whats_my_species_yaml)
    species = datahandling.load_species(sample["properties"]["species"])
    
    results = []

    try:
        detected = whats_my_species["summary"]["percent_classified_species_1"] + \
            whats_my_species["summary"]["percent_unclassified"]
        if detected < MINSPECIES:
            results.append({
                "name": "whats_my_species.minspecies",
                "reason": "value",
                "status": "fail"
            })
        else:
            results.append({
                "name": "whats_my_species.minspecies",
                "status": "pass",
                "reason": "",
            })
    except KeyError:
        results.append({
            "name": "whats_my_species.minspecies",
            "reason": "missing",
            "status": "KeyError"
        })
    

    # Submitted == detected
    try:
        detected = whats_my_species["summary"]["name_classified_species_1"]
        submitted = sample["properties"]["provided_species"]
        if submitted is None:
            results.append({
                "name": "whats_my_species.submitted==detected",
                "reason": "missing",
                "status": "undefined"
            })
        else:
            if submitted != detected:
                results.append({
                    "name": "whats_my_species.submitted==detected",
                    "status": "fail",
                    "reason": "value"
                })
            else:
                results.append({
                    "name": "whats_my_species.submitted==detected",
                    "status": "pass",
                    "reason": "",
                })
    except KeyError:
        results.append({
            "name": "whats_my_species.submitted==detected",
            "reason": "KeyError",
            "status": "fail"
        })


    # Provided not in DB ## NOT CHECKED HERE ?

    # Genome size check for 1x    
    try:
        size = qcquickie["summary"]["bin_length_at_1x"]
        min_size = species["min_length"]
        max_size = species["max_length"]
        if min_size < size < max_size:
            results.append({
                "name": "qcquickie.1xgenomesize",
                "status": "pass",
                "reason": ""
            })
        else:
            results.append({
                "name": "qcquickie.1xgenomesize",
                "status": "warning",
                "reason": "value"
            })
    except KeyError:
        results.append({
            "name": "qcquickie.1xgenomesize",
            "reason": "KeyError",
            "status": "fail"
        })

    # Genome size difference 1x 25x
    try:
        size_1x = qcquickie["summary"]["bin_length_at_1x"]
        size_25x = qcquickie["summary"]["bin_length_at_25x"]
        max_diff = species["max_length"] * 0.25 # Placeholder
        if size_1x - size_25x < max_diff:
            results.append({
                "name": "qcquickie.1x25xsizediff",
                "status": "pass",
                "reason": ""
            })
        else:
            results.append({
                "name": "qcquickie.1x25xsizediff",
                "status": "warning",
                "reason": "value"
            })
    except KeyError:
        results.append({
            "name": "qcquickie.1x25xsizediff",
            "reason": "KeyError",
            "status": "fail"
        })
    
    # Contig number
    try:
        contigs = qcquickie["summary"]["bin_contigs_at_25x"]
        if contigs < CONTIGMAX:
            results.append({
                "name": "qcquickie.contigmax",
                "status": "pass",
                "reason": ""
            })
        else:
            results.append({
                "name": "qcquickie.contigmax",
                "status": "fail",
                "reason": "value"
            })
    except KeyError:
        results.append({
            "name": "qcquickie.contigmax",
            "reason": "KeyError",
            "status": "fail"
        })

    # Average coverage
    try:
        coverage = qcquickie["summary"]["bin_coverage_at_1x"]
        if coverage < AVGCOVERAGE_FAIL:
            results.append({
                "name": "qcquickie.avgcoverage",
                "status": "fail",
                "reason": "value"
            })
        elif coverage < AVGCOVERAGE_WARN:
            results.append({
                "name": "qcquickie.avgcoverage",
                "status": "warning",
                "reason": "value"
            })
        else:
            results.append({
                "name": "qcquickie.avgcoverage",
                "status": "pass",
                "reason": ""
            })
    except KeyError:
        results.append({
            "name": "qcquickie.avgcoverage",
            "reason": "KeyError",
            "status": "fail"
        })

    # Minimum number of reads
    try:
        num_reads = qcquickie["summary"]["filtered_reads_num"]

        if num_reads < NUMREADS_FAIL:
            results.append({
                "name": "qcquickie.numreads",
                "status": "fail",
                "reason": "value"
            })
        elif num_reads < NUMREADS_WARN:
            results.append({
                "name": "qcquickie.numreads",
                "status": "warning",
                "reason": "value"
            })
        else:
            results.append({
                "name": "qcquickie.numreads",
                "status": "pass",
                "reason": ""
            })
    except KeyError:
        results.append({
            "name": "qcquickie.numreads",
            "reason": "KeyError",
            "status": "fail"
        })
    
    assemblatron = datahandling.load_sample_component(assemblatron_yaml)
    if len(assemblatron_yaml) > 0:
        try:
            size = assemblatron["summary"]["bin_length_at_1x"]
            min_size = species["min_length"]
            max_size = species["max_length"]
            if min_size < size < max_size:
                results.append({
                    "name": "assemblatron.1xgenomesize",
                    "status": "pass",
                    "reason": ""
                })
            else:
                results.append({
                    "name": "assemblatron.1xgenomesize",
                    "status": "warning",
                    "reason": "value"
                })
        except KeyError:
            results.append({
                "name": "assemblatron.1xgenomesize",
                "reason": "KeyError",
                "status": "fail"
            })

        # Genome size difference 1x 25x
        try:
            size_1x = assemblatron["summary"]["bin_length_at_1x"]
            size_25x = assemblatron["summary"]["bin_length_at_25x"]
            max_diff = species["max_length"] * 0.25 # Placeholder
            if size_1x - size_25x < max_diff:
                results.append({
                    "name": "assemblatron.1x25xsizediff",
                    "status": "pass",
                    "reason": ""
                })
            else:
                results.append({
                    "name": "assemblatron.1x25xsizediff",
                    "status": "warning",
                    "reason": "value"
                })
        except KeyError:
            results.append({
                "name": "assemblatron.1x25xsizediff",
                "reason": "KeyError",
                "status": "fail"
            })
        
        # Contig number
        try:
            contigs = assemblatron["summary"]["bin_contigs_at_25x"]
            if contigs < CONTIGMAX:
                results.append({
                    "name": "assemblatron.contigmax",
                    "status": "pass",
                    "reason": ""
                })
            else:
                results.append({
                    "name": "assemblatron.contigmax",
                    "status": "fail",
                    "reason": "value"
                })
        except KeyError:
            results.append({
                "name": "assemblatron.contigmax",
                "reason": "KeyError",
                "status": "fail"
            })

        # Average coverage
        try:
            coverage = assemblatron["summary"]["bin_coverage_at_1x"]
            if coverage < AVGCOVERAGE_FAIL:
                results.append({
                    "name": "assemblatron.avgcoverage",
                    "status": "fail",
                    "reason": "value"
                })
            elif coverage < AVGCOVERAGE_WARN:
                results.append({
                    "name": "assemblatron.avgcoverage",
                    "status": "warning",
                    "reason": "value"
                })
            else:
                results.append({
                    "name": "assemblatron.avgcoverage",
                    "status": "pass",
                    "reason": ""
                })
        except KeyError:
            results.append({
                "name": "assemblatron.avgcoverage",
                "reason": "KeyError",
                "status": "fail"
            })

        # Minimum number of reads
        try:
            num_reads = assemblatron["summary"]["filtered_reads_num"]

            if num_reads < NUMREADS_FAIL:
                results.append({
                    "name": "assemblatron.numreads",
                    "status": "fail",
                    "reason": "value"
                })
            elif num_reads < NUMREADS_WARN:
                results.append({
                    "name": "assemblatron.numreads",
                    "status": "warning",
                    "reason": "value"
                })
            else:
                results.append({
                    "name": "assemblatron.numreads",
                    "status": "pass",
                    "reason": ""
                })
        except KeyError:
            results.append({
                "name": "assemblatron.numreads",
                "reason": "KeyError",
                "status": "fail"
            })

    datadump_dict = datahandling.load_sample_component(sample_component)
    datadump_dict["summary"] = generate_summary(results)
    datadump_dict["results"] = results
    datahandling.save_sample_component(datadump_dict, sample_component)
    return 0

script__test_testomatic(snakemake.input.qcquickie_yaml,
                        snakemake.params.assemblatron_yaml,
                        snakemake.params.whats_my_species_yaml,
                        snakemake.params.sample,
                        snakemake.params.sample_component)
