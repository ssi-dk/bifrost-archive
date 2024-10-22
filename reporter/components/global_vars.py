import collections
import math

PLOTS = collections.OrderedDict()

PLOTS["assemblatron.bin_length_at_1x"] = {
    "projection": "assemblatron.bin_length_at_1x"
}
PLOTS["assemblatron.bin_length_at_10x"] = {
    "projection": "assemblatron.bin_length_at_10x"
}
PLOTS["assemblatron.bin_length_at_25x"] = {
    "projection": "assemblatron.bin_length_at_25x"
}
def assemblatron_diff(res):
    if "assemblatron.bin_length_at_1x" in res and "assemblatron.bin_length_at_10x" in res:
        res["assemblatron.bin_length_1x_10x_diff"] = res["assemblatron.bin_length_at_1x"] - \
            res["assemblatron.bin_length_at_10x"]
    else:
        res["assemblatron.bin_length_1x_10x_diff"] = math.nan
    return res

PLOTS["assemblatron.bin_length_1x_10x_diff"] = {
    "projection": "assemblatron.bin_length_1x_10x_diff",
        "func": assemblatron_diff
    }

PLOTS["assemblatron.bin_coverage_at_1x"] = {
    "projection": "assemblatron.bin_coverage_at_1x"
}
PLOTS["assemblatron.bin_coverage_at_10x"] = {
    "projection": "assemblatron.bin_coverage_at_10x"
}
PLOTS["assemblatron.bin_coverage_at_25x"] = {
    "projection": "assemblatron.bin_coverage_at_25x"
}
PLOTS["assemblatron.bin_contigs_at_1x"] = {
    "projection": "assemblatron.bin_contigs_at_1x"
}
PLOTS["assemblatron.bin_contigs_at_10x"] = {
    "projection": "assemblatron.bin_contigs_at_10x"
}

def assemblatron_contig_diff(res):
    if "assemblatron.bin_contigs_at_1x" in res and "assemblatron.bin_contigs_at_10x" in res:
        res["assemblatron.bin_contigs_1x_10x_diff"] = res["assemblatron.bin_contigs_at_1x"] - \
            res["assemblatron.bin_contigs_at_10x"]
    else:
        res["assemblatron.bin_contigs_1x_10x_diff"] = math.nan
    return res


PLOTS["assemblatron.bin_contigs_1x_10x_diff"] = {
    "projection": "assemblatron.bin_contigs_1x_10x_diff",
    "func": assemblatron_contig_diff
}

PLOTS["assemblatron.bin_contigs_at_25x"] = {
    "projection": "assemblatron.bin_contigs_at_25x"
}
PLOTS["assemblatron.N50"] = {
    "projection": "assemblatron.N50"
}

DEFAULT_PLOT = "assemblatron.bin_length_at_1x"


FUNCS = [assemblatron_diff, assemblatron_contig_diff]


COLUMNS = [
    {
        "name": "Name",
        "id": "name"
    },
    {
        "name": "QC_action",
        "id": "ssi_stamper.assemblatron:action"
    },
    {
        "name": "Comments",
        "id": "sample_sheet.Comments"
    },
    {
        "name": "Supplying_lab",
        "id": "sample_sheet.group"
    },
    {
        "name": "Provided_Species",
        "id": "properties.provided_species"
    },
    {
        "name": "Detected Species",
        "id": "properties.detected_species"
    },
    {
        "name": "Genome_size_1x",
        "id": "assemblatron.bin_length_at_1x"
    },
    {
        "name": "Genome_size_10x",
        "id": "assemblatron.bin_length_at_10x"
    },
    {
        "name": "G_size_difference_1x_10",
        "id": "ssi_stamper.assemblatron:1x10xsizediff_text"
    },
    {
        "name": "Avg_coverage",
        "id": "assemblatron.bin_coverage_at_1x"
    },
    {
        "name": "Num_contigs",
        "id": "assemblatron.bin_contigs_at_1x"
    },
    {
        "name": "Ambiguous_sites",
        "id": "assemblatron.snp_filter_10x_10%"
    },
    {
        "name": "Num_reads",
        "id": "assemblatron.filtered_reads_num"
    },
    {
        "name": "mlst_type",
        "id": "analyzer_mlst_type"
    },
    {
        "name": "mlst_alleles",
        "id": "analyzer_mlst_alleles"
    },
    {
        "name": "Main_species_plus_undetermined_read_percent",
        "id": "ssi_stamper.whats_my_species:minspecies_text"
    },
    {
        "name": "Unclassified_reads",
        "id": "whats_my_species.percent_unclassified"
    },
    {
        "name": "DB_ID",
        "id": "_id"
    },
    {
        "name": "Failed_tests",
        "id": "ssi_stamper_failed_tests"
    }

]

plot_values = [
    {
        "name": "Genome_size_1x",
        "id": "assemblatron.bin_length_at_1x",
        "limits": [1500000, 6000000]
    },
    {
        "name": "Genome_size_10x",
        "id": "assemblatron.bin_length_at_10x",
        "limits": [1500000, 6000000],
        "xaxis": "x"
    },
    {
        "name": "G_size_difference_1x_10",
        "id": "ssi_stamper.assemblatron:1x10xsizediff_text",
        "limits": [0, 260000]
    },
    {
        "name": "Avg_coverage",
        "id": "assemblatron.bin_coverage_at_1x",
        "limits": [0, 200]
    },
    {
        "name": "Contig_num_1x",
        "id": "assemblatron.bin_contigs_at_1x",
        "limits": [0, 700]
    },
    {
        "name": "Num_reads",
        "id": "assemblatron.filtered_reads_num",
        "limits": [1000, 8000000]
    },
    {
        "name": "Main_sp_plus_unclassified",
        "id": "ssi_stamper.whats_my_species:minspecies_text",
        "limits": [0.75, 1]
    },
    {
        "name": "Unclassified_reads",
        "id": "whats_my_species.percent_unclassified",
        "limits": [0, 0.25]
    }
]
