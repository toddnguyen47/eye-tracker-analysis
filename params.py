import os

cur_dir = os.getcwd()

# Required columns to collapse
REQ_COLUMNS_TO_COLLAPSE = ["FixationSeq", "FixationX", "FixationY",
                           "FixationStart", "FixationDuration"]

# Collapsed filename
COLLAPSED_CSV_FILENAME = os.path.join("C:/Users/ToddNguyen/Documents/Research/collapsed/7_output_collapsed_graphlabel.csv")

# Input extended filename
# INPUT_CSV_FILENAME = os.path.join(cur_dir, "sample_data/p7_extended_DONOTINCLUDE.csv")
INPUT_CSV_FILENAME = "C:/Users/ToddNguyen/Documents/Research/13_output.csv"

# Main output file
CALCULATED_OUTPUT = os.path.join(cur_dir, "outputs/calculated_output.csv")

# File with graph information
GRAPH_INFO_FILE = os.path.join("../../../Documents/Research/CompletionTime.csv")

# Collapsed file to label
COLLAPSED_FILE_TO_LABEL = ("C:/Users/ToddNguyen/Documents/Research/collapsed/13_output_collapsed.csv")
