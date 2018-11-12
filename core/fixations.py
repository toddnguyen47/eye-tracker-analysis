import pandas as pd
import params  # local params.py file
import math
import os

# column_names = ["StudyName", "ExportDate", "Name", "Age", "Gender", "StimulusName", "SlideType",
#                 "EventSource", "UTCTimestamp", "Timestamp", "MediaTime", "TimeSignal", "GazeLeftx",
#                 "GazeLefty", "GazeRightx", "GazeRighty", "PupilLeft", "PupilRight", "DistanceLeft",
#                 "DistanceRight", "CameraLeftX", "CameraLeftY", "CameraRightX", "CameraRightY",
#                 "ValidityLeft", "ValidityRight", "GazeX", "GazeY", "GazeAOI", "InterpolatedGazeX",
#                 "InterpolatedGazeY", "GazeEventType", "GazeVelocityAngle", "SaccadeSeq", "SaccadeStart",
#                 "SaccadeDuration", "FixationSeq", "FixationX", "FixationY", "FixationStart",
#                 "FixationDuration", "FixationAOI", "PostMarker", "Annotation", "LiveMarker", "KeyStroke",
#                 "MarkerText", "SceneType", "SceneOutput", "SceneParent Current_task"]


def read_in_csv(csv_file):
    df = pd.read_csv(csv_file, sep=",", header=6, index_col=False)

    print(df.to_string())

    # total_num_fixations = get_total_num_fixations(df)
    # fixation_duration_col = df['FixationDuration']
    # total_fixation_duration = fixation_duration_col.sum()
    # mean_fixation_duration = fixation_duration_col.mean()
    # stddev_fixation_duration = fixation_duration_col.std(ddof=1)  # delta degrees of freedom

    # # Output to text and console
    # output = []
    # output.append("Total number of fixations: {}".format(total_num_fixations))
    # output.append("Total fixation duration: {}".format(total_fixation_duration))
    # output.append("Mean fixation duration: {}".format(mean_fixation_duration))
    # output.append("Standard deviation fixation duration: {}".format(stddev_fixation_duration))
    # output_to_txt(output, write_to_console=True)


def get_total_num_fixations(pd_dataframe):
    '''
    Obtain the total number of fixations.

    # Arguments
    pd_dataframe    -> The pandas dataframe with CSV information
    '''
    # Fill empty columns with -1 for easier parsing
    na_fill_value = -1

    fixations = pd_dataframe['FixationDuration'].fillna(value=na_fill_value).values.tolist()

    prev_value = na_fill_value
    fixation_count = 0

    for fixation in fixations:
        if fixation != na_fill_value and fixation != prev_value:
            fixation_count += 1
            prev_value = fixation

    return fixation_count


def collapse_to_fixations(csv_file):
    pd_dataframe = pd.read_csv(csv_file, sep=",", header=6, index_col=False)
    overwrite = "y"

    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    if (os.path.exists(params.COLLAPSED_CSV_FILENAME)):
        overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(params.COLLAPSED_CSV_FILENAME))

    if overwrite.lower() == "y":
        new_df = pd.DataFrame(columns=pd_dataframe.columns)
        fixation_included = set()
        # Iterate over all the rows
        # Reference: https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
        for index, row in pd_dataframe.iterrows():
            # Only care about rows with a FixationSeq value
            fixation_seq = row['FixationSeq']
            # Ignore all NaN values and only add if the fixation is not included yet
            if not math.isnan(fixation_seq) and fixation_seq not in fixation_included:
                fixation_included.add(fixation_seq)
                new_df_len = len(new_df.index)
                new_df.loc[new_df_len] = row

        new_df.to_csv(params.COLLAPSED_CSV_FILENAME, index=False)
        print("Finished exporting to {}".
              format(params.COLLAPSED_CSV_FILENAME).replace("\\", "/"))
    else:
        print("Exiting...")
