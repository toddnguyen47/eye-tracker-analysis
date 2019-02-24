import pandas as pd
import math
import os
import time
from core import utils


def collapse_to_fixations(input_file, output_file):
    """
    Collapse a larger input file to a smaller output file with only one fixation per line.

    :param input_file: The large, uncollapsed CSV file
    :param output_file: The collapsed CSV file
    """
    print("Collapsing...")
    pd_dataframe = pd.read_csv(input_file, sep=",", header=6, index_col=False)
    print("Finished loading in \"{}\" file".format(input_file))

    overwrite = "y"
    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    if (os.path.exists(output_file)):
        overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(output_file).replace("\\", "/"))

    if overwrite.lower() == "y":
        new_df = pd.DataFrame(columns=pd_dataframe.columns)
        fixation_included = set()
        # Iterate over all the rows
        # Reference: https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
        num_rows = len(pd_dataframe.index)
        count = 0
        print("Iterating over every row:")
        starttime = time.time()
        for index, row in pd_dataframe.iterrows():
            # Only care about rows with a FixationSeq value
            fixation_seq = row['FixationSeq']
            # Ignore all NaN values and only add if the fixation is not included yet
            if not math.isnan(fixation_seq) and fixation_seq not in fixation_included:
                fixation_included.add(fixation_seq)
                new_df_len = len(new_df.index)
                new_df.loc[new_df_len] = row

            curtime = time.time()
            elapsed_time = curtime - starttime
            count += 1
            progress = utils.progress_bar(count, num_rows, elapsed_time)
            print(progress, end="\r")

        print("")
        new_df.to_csv(output_file, index=False)
        print("Finished exporting to {}".
              format(output_file).replace("\\", "/"))
    else:
        print("Exiting...")
