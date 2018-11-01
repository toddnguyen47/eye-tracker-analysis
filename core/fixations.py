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

    collapse_to_fixations(df)

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


def collapse_to_fixations(pd_dataframe):
    # Export to csv file
    # If file exists and user does not want to overwrite, do nothing
    if (os.path.exists(params.COLLAPSED_CSV_FILENAME)):
        overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): ".format(params.COLLAPSED_CSV_FILENAME))
        # if No
        if overwrite.lower() == "n":
            print("Exiting...")
            return

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
            new_df = new_df.append(row)

    new_df.to_csv(params.COLLAPSED_CSV_FILENAME)
    print("Finished exporting")


def output_to_txt(list_of_str, write_to_console=False):
    with open("outputs/output.txt", "w") as file:
        for string1 in list_of_str:
            file.write(string1)
            file.write("\n")

            if write_to_console:
                print(string1)


def get_saccade_length(csv_file):
    df = pd.read_csv(csv_file, sep=",", header=0, index_col=False)
    list_of_coordinates = []

    for index, row in df.iterrows():
        x_coord = row['FixationX']
        y_coord = row['FixationY']
        cur_task = row['Current_task']
        list_of_coordinates.append([cur_task, x_coord, y_coord])
    
    filename = os.path.join(os.getcwd(), "outputs", "saccades.csv")
    with open(filename, "w") as file:
        file.write("Current_task,FixationX,FixationY,SaccadeLength\n")
        # first fixation has no saccade length
        first_fixation = list_of_coordinates[0]
        file.write(",".join((str(first_fixation[0]), str(first_fixation[1]),
                             str(first_fixation[2]), "N/A")))
        file.write("\n")

        # Skip the first fixation since we cannot calculate the saccade length
        # for the first fixation
        for i in range(1, len(list_of_coordinates)):
            cur_fixation  = list_of_coordinates[i]
            prev_fixation = list_of_coordinates[i - 1]
            
            # Get the x and y coordinates of current fixation and previous fixation
            cur_x  = cur_fixation[1]
            cur_y  = cur_fixation[2]
            prev_x = prev_fixation[1]
            prev_y = prev_fixation[2]

            # Use the distance formula to calculate saccade length
            # c = sqrt(a^2 + b^2)
            x_dist = cur_x - prev_x
            y_dist = cur_y - prev_y
            saccade_length = math.sqrt(x_dist**2 + y_dist**2)

            # Write to csv
            # Current_task, x, y, saccade_length
            file.write(",".join((str(cur_fixation[0]), str(cur_x),
                                 str(cur_y), str(saccade_length))))
            file.write("\n")

    print("Finished calculating saccades")
