import os

cur_dir = os.getcwd()

# Required columns to collapse
REQ_COLUMNS_TO_COLLAPSE = ["FixationSeq", "FixationX", "FixationY",
                           "FixationStart", "FixationDuration"]

# Collapsed filename
COLLAPSED_CSV_FILENAME = os.path.join(cur_dir, "sample_data/p7_collapsed_2.csv")

# Input extended filename
INPUT_CSV_FILENAME = os.path.join(cur_dir, "sample_data/p7_extended_DONOTINCLUDE.csv")

# Main output file
MAIN_OUTPUT_FILE = os.path.join(cur_dir, "outputs/calculated_output.csv")
