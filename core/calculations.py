"""
This python file will call functions to calculate:
    * Fixations length? TODO
    * Saccade length
    * Saccade absolute angle
    * Saccade relative angle
And export it to a file
"""
import pandas as pd
import params
import core.saccades as saccades
import os

HEADERS = [ "Current_task", "FixationX", "FixationY", "SaccadeLength", "SaccadeAbsoluteAngleDegrees",
            "SaccadeRelativeAngleDegrees"]


def calculate(csv_file):
    """
    Calculate a collapsed file.

    # Arguments
    csv_file    -> Collapsed csv file
    """
    overwrite = "y"
    # If file exists
    if (os.path.exists(params.COLLAPSED_CSV_FILENAME)):
        overwrite = input("\"{}\" exists. Would you like to overwrite? (Y/N): "
                          .format(params.COLLAPSED_CSV_FILENAME).replace("\\", "/"))

    if (overwrite.strip().lower() == "y"):
        df = pd.read_csv(csv_file)
        cur_task_list = []
        coords_list = []

        # Extracct current_task and coords first
        for index, row in df.iterrows():
            cur_task = row['Current_task']
            x_coord = row['FixationX']
            y_coord = row['FixationY']

            cur_task_list.append(cur_task)
            coords_list.append([x_coord, y_coord])

        # Calculate the saccade length, saccade absolute angle, and saccade relative angle
        saccade_lengths_list = []
        saccade_abs_angles_list = []
        saccade_rel_angles_list = []

        max_len = len(coords_list)
        for i in range(max_len):
            cur_task = cur_task_list[i]
            cur_coords = coords_list[i]
            saccade_length = 0.0
            saccade_absolute_angle = 0.0
            saccade_relative_angle = 0.0

            # If i is 0, we cannot calculate any angles nor lengths
            if (i - 1 >= 0):
                prev_coords = coords_list[i - 1]
                saccade_length = saccades.calc_saccade_length(cur_coords, prev_coords)
                saccade_absolute_angle = saccades.calc_abs_angle(cur_coords, prev_coords, use_degrees=True)

                # If it is the last i, we cannot calculate relative angles
                if (i + 1 < max_len):
                    next_coords = coords_list[i + 1]
                    saccade_relative_angle = saccades.calc_rel_angle(cur_coords, prev_coords, next_coords, use_degrees=True)

            saccade_lengths_list.append(saccade_length)
            saccade_abs_angles_list.append(saccade_absolute_angle)
            saccade_rel_angles_list.append(saccade_relative_angle)

        df['Saccade_length'] = saccade_lengths_list
        df['Saccade_absolute_angle'] = saccade_abs_angles_list
        df['Saccade_relative_angle'] = saccade_rel_angles_list
        df.to_csv(params.COLLAPSED_CSV_FILENAME, index=False)
        print("Finished writing to {}".format(params.COLLAPSED_CSV_FILENAME.replace("\\", "/")))

    else:
        print("Exiting...")


def output_to_txt(list_of_str, write_to_console=False):
    with open("outputs/output.txt", "w") as file:
        for string1 in list_of_str:
            file.write(string1)
            file.write("\n")

            if write_to_console:
                print(string1)
