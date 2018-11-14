import os

cur_dir = os.getcwd()

# Required columns to collapse
# REQ_COLUMNS_TO_COLLAPSE = ["FixationSeq", "FixationX", "FixationY",
#                            "FixationStart", "FixationDuration"]

# Input extended filename
# INPUT_CSV_FILENAME = os.path.join(cur_dir, "sample_data/p7_extended_DONOTINCLUDE.csv")
INPUT_CSV_FILENAME = "Z:/DocumentsAndStuff/Documents/Research/20_output.csv"

# Collapsed filename
COLLAPSED_CSV_FILENAME = os.path.join(cur_dir, "outputs/20_collapsed.csv")

# Graph information
GRAPH_INFO_FILE = "Z:\DocumentsAndStuff\Downloads\CompletionTime.csv"


def progress_bar(current, total, elapsed_time, char_to_use="#"):
    """
    Return a string that details the current progress using hashtags.
    """
    import math
    max_hashtag = 30
    num_hashtags = math.floor(current / total * max_hashtag)
    s = ""
    for i in range(num_hashtags):
        s = "".join((s, char_to_use))
    for i in range(max_hashtag - num_hashtags):
        s = "".join((s, " "))
    
    return_string = "[{}] {:.2%}, {:.2f} seconds collapsed".format(s, current / total, elapsed_time)
    return return_string
