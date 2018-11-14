import pandas as pd
import params  # local params.py file
import math
import os
import time


def collapse_to_fixations(csv_file):
    print("Collapsing...")
    pd_dataframe = pd.read_csv(csv_file, sep=",", header=6, index_col=False)
    print("Finished loading in \"{}\" file".format(csv_file))
    
    overwrite = "y"
    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    if (os.path.exists(params.COLLAPSED_CSV_FILENAME)):
        overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(params.COLLAPSED_CSV_FILENAME).replace("\\", "/"))

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
            progress = params.progress_bar(count, num_rows, elapsed_time)
            print(progress, end="\r")

        print("")
        new_df.to_csv(params.COLLAPSED_CSV_FILENAME, index=False)
        print("Finished exporting to {}".
              format(params.COLLAPSED_CSV_FILENAME).replace("\\", "/"))
    else:
        print("Exiting...")
