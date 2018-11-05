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

HEADERS = [ "Current_task", "FixationX", "FixationY", "SaccadeLength", "SaccadeAbsoluteAngle",
            "SaccadeRelativeAngle"]


def calculate(csv_file):
    """
    Calculate a collapsed file.

    # Arguments
    csv_file    -> Collapsed csv file
    """
    df = pd.read_csv(csv_file)
    cur_task_list = []
    coords_list = []

    # Start writing to a csv file
    with open(params.MAIN_OUTPUT_FILE, "w") as file:
        for header in HEADERS:
            file.write("".join((header, ",")))
        file.write("\n")


    # Extracct current_task and coords first
    for index, row in df.iterrows():
        cur_task = row['Current_task']
        x_coord = row['FixationX']
        y_coord = row['FixationY']

        cur_task_list.append(cur_task)
        coords_list.append([x_coord, y_coord])

    with open(params.MAIN_OUTPUT_FILE, "a") as file:
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
                saccade_absolute_angle = saccades.calc_abs_angle(cur_coords, prev_coords)

                # If it is the last i, we cannot calculate relative angles
                if (i + 1 < max_len):
                    next_coords = coords_list[i + 1]
                    saccade_relative_angle = saccades.calc_rel_angle(cur_coords, prev_coords, next_coords)

            csv_file_str = ",".join((   cur_task, str(cur_coords[0]), str(cur_coords[1]),
                                        str(saccade_length), str(saccade_absolute_angle),
                                        str(saccade_relative_angle)))
            file.write(csv_file_str)
            file.write("\n")


def output_to_txt(list_of_str, write_to_console=False):
    with open("outputs/output.txt", "w") as file:
        for string1 in list_of_str:
            file.write(string1)
            file.write("\n")

            if write_to_console:
                print(string1)
