import pandas as pd

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

    total_num_fixations = get_total_num_fixations(df)
    fixation_duration_col = df['FixationDuration']
    total_fixation_duration = fixation_duration_col.sum()
    mean_fixation_duration = fixation_duration_col.mean()
    stddev_fixation_duration = fixation_duration_col.std(ddof=1)  # delta degrees of freedom

    # Output to text and console
    output = []
    output.append("Total number of fixations: {}".format(total_num_fixations))
    output.append("Total fixation duration: {}".format(total_fixation_duration))
    output.append("Mean fixation duration: {}".format(mean_fixation_duration))
    output.append("Standard deviation fixation duration: {}".format(stddev_fixation_duration))
    output_to_txt(output, write_to_console=True)


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


def output_to_txt(list_of_str, write_to_console=False):
    with open("outputs/output.txt", "w") as file:
        for string1 in list_of_str:
            file.write(string1)
            file.write("\n")

            if write_to_console:
                print(string1)
