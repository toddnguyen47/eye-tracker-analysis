import os

cur_dir = os.getcwd()

# Required columns to collapse
# REQ_COLUMNS_TO_COLLAPSE = ["FixationSeq", "FixationX", "FixationY",
#                            "FixationStart", "FixationDuration"]

# Input extended filename
# INPUT_CSV_FILENAME = os.path.join(cur_dir, "sample_data/p7_extended_DONOTINCLUDE.csv")
INPUT_CSV_FILENAME = "Z:/DocumentsAndStuff/Documents/Research/7_output.csv"

# Collapsed filename
COLLAPSED_CSV_FILENAME = os.path.join(cur_dir, "outputs/collapsed.csv")

# Graph information
GRAPH_INFO_FILE = "Z:\DocumentsAndStuff\Downloads\CompletionTime.csv"
