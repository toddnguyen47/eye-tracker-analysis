import os
import pandas as pd
import core.utils as utils
import numpy as np


class GetStats:
    def __init__(self):
        self._header_row_hashset = {}
        self._col_names_list = ["FixationDuration", "Saccade_length", "Saccade_absolute_angle",
                                "Saccade_relative_angle"]
        self._header_per_task = {}


    def get_stats_all_users(self, file_dir, outfile):
        """
        Get stats for all users and put it in the outfile.
        :param file_dir: The file directory
        :param outfile: The outfile to export to a CSV file
        """
        all_stats_list = []
        for file in os.listdir(file_dir):
            if file.endswith("csv"):
                print("Calculating stats for file {}...".format(file))
                filepath = os.path.join(file_dir, file)
                file_stats = self.get_stats_per_file(filepath)

                # Should never happen
                if len(self._header_row_hashset) != len(file_stats):
                    raise ValueError("Header row set and file_stats list should have the same length")

                all_stats_list.append(file_stats)

        # Output
        with open(outfile, "w") as file:
            file.write(",".join(self._header_row_hashset.keys()))
            file.write("\n")
            for stats in all_stats_list:
                file.write(",".join(stats))
                file.write("\n")

        print("Finished writing to {}".format(outfile.replace("\\", "/")))


    def get_stats_per_file(self, full_path_to_csv_file):
        """
        Get the stats per file and return it in a list.
        :param full_path_to_csv_file: The full path to the CSV file.
        :return: A list of the stats, as well as any new column headers added to
        self._header_row_hashset
        """
        # Get the participant number
        participant_id = ""
        for char in full_path_to_csv_file.replace("\\", "/").split("/")[-1]:
            if char.isdigit():
                participant_id = "".join((participant_id, char))

        self._header_row_hashset["Participant"] = None
        return_list = [participant_id]

        input_df = pd.read_csv(full_path_to_csv_file, index_col=False)

        # Get the basic stats: sum, average, and standard deviation
        for col_name in self._col_names_list:
            column = input_df[col_name]

            # Add the sum headers + info to the main list
            s = "{}_Sum".format(col_name)
            s2 = column.abs().sum().item()
            self._header_row_hashset[s] = None
            return_list.append(str(s2))

            # Add the average headers + info to the main list
            s = "{}_Average".format(col_name)
            s2 = column.abs().mean().item()
            self._header_row_hashset[s] = None
            return_list.append(str(s2))

            # Add in standard deviation
            s = "{}_StandardDeviation".format(col_name)
            s2 = column.abs().std().item()
            self._header_row_hashset[s] = None
            return_list.append(str(s2))

        # Get AOI statistics, such as proportions of fixation per AOI
        # Get the AOI file data
        json_aoi_data = utils.load_in_aoi_json()
        aoi_info_list = self.get_stats_per_aoi(input_df, json_aoi_data)
        # Append AOI info list to our current list
        return_list.extend(aoi_info_list)

        return return_list


    def get_stats_per_aoi(self, pd_dataframe, aoi_json_data):
        """
        Get stats per Area of Interest (AOI).
        :param pd_dataframe: The pandas dataframe with the CSV file of current participant
        :param aoi_json_data: The JSON file with the AOI information.
        :return: A list of stats, plus any new addititions to self.__header_row_hashset
        """
        # Create a temporary dictionary for this function
        dict1 = {"TotalNumFixations": 0, "TotalNumFixationsInAOI": 0, "TotalProportionsOfFixationsInAOI": 0}

        task_col = pd_dataframe["Current_task"]
        aoi_col = pd_dataframe["AOI"]
        fixation_duration = pd_dataframe["FixationDuration"]

        temp_data = aoi_json_data["HighBar"]
        aoi_list = []
        # Now, we will use our HashSet dict as temporary storage for AOI-related information
        # Initialize the HashSet dict
        for key in temp_data.keys():
            key_2 = "_".join((key, "AOI"))
            aoi_list.append(key_2)
            dict1[key_2 + "_NumberOfFixations"] = 0
            dict1[key_2 + "_FixationDurationSum"] = 0
            dict1[key_2 + "_FixationDurationMean"] = 0
            dict1[key_2 + "_LongestFixationInAOI"] = 0
            dict1[key_2 + "_ProportionOfTotalFixations"] = 0
            dict1[key_2 + "_ProportionOfTotalFixationDuration"] = 0

        total_fixation_duration = 0

        for i in range(len(task_col)):
            cur_task = task_col[i]
            cur_aoi = str(aoi_col[i])
            # Ignore all pretask and any tasks that are not in the AOI
            if cur_task.lower() != "pretask".lower():
                dict1["TotalNumFixations"] += 1
                if cur_aoi.lower() != "nan".lower():
                    dict1["TotalNumFixationsInAOI"] += 1

                    # cur_task_graph = list(graph_col[i].lower())
                    # # Lowercase cur task graph, then uppercase only the first character
                    # cur_task_graph[0] = cur_task_graph[0].upper()
                    # cur_task_graph = "".join(cur_task_graph)

                    # h_or_l = cur_task[1]
                    # high_or_low = "High" if h_or_l.lower() == "h".lower() else "Low"
                    # cur_task_key = "".join((high_or_low, cur_task_graph))

                    # Current Task Fixation Duration
                    cur_task_fixation_duration = fixation_duration[i].item()
                    total_fixation_duration += cur_task_fixation_duration

                    num_fixations_1 = dict1[cur_aoi + "_NumberOfFixations"] + 1
                    fix_duration_1 = dict1[cur_aoi + "_FixationDurationSum"] +\
                                     cur_task_fixation_duration
                    # To prevent dividing by zero
                    if num_fixations_1 == 0:
                        mean_fix_duration_1 = 0
                    else:
                        mean_fix_duration_1 = fix_duration_1 / num_fixations_1

                    dict1[cur_aoi + "_NumberOfFixations"] = num_fixations_1
                    dict1[cur_aoi + "_FixationDurationSum"] = fix_duration_1
                    dict1[cur_aoi + "_FixationDurationMean"] = \
                        round(mean_fix_duration_1, 4)

                    # Get the longest fixation in AOI
                    if dict1[cur_aoi + "_LongestFixationInAOI"] < cur_task_fixation_duration:
                        dict1[cur_aoi + "_LongestFixationInAOI"] = cur_task_fixation_duration

        # Obtain Post-Stats
        for key in aoi_list:
            # Get the proportion of total number of fixations in AOI
            proportion_key = "_ProportionOfTotalFixations"
            if dict1["TotalNumFixations"] == 0:
                dict1[key + proportion_key] = 0
            else:
                proportion_value = dict1[key + "_NumberOfFixations"] / dict1["TotalNumFixations"]
                proportion_value = round(proportion_value, 6)
                dict1[key + proportion_key] = proportion_value

            # Get the proportion of total number of fixation duration
            proportion_key = "_ProportionOfTotalFixationDuration"
            if total_fixation_duration == 0:
                dict1[key + proportion_key] = 0
            else:
                proportion_value = dict1[key + "_FixationDurationSum"] / total_fixation_duration
                proportion_value = round(proportion_value, 6)
                dict1[key + proportion_key] = proportion_value

        # Get total proportions of fixations in aoi
        if dict1["TotalNumFixations"] != 0:
            dict1["TotalProportionsOfFixationsInAOI"] = dict1["TotalNumFixationsInAOI"] / dict1["TotalNumFixations"]

        # Add keys to list, then add values to return list
        return_list = []
        for key in dict1.keys():
            self._header_row_hashset[key] = None
            return_list.append(str(dict1[key]))

        return return_list


    def get_stats_per_task(self, full_path_to_csv_file, csv_output):
        """
        Get the stats per task.
        :param full_path_to_csv_file: The path where the input files are.
        :param csv_output: Name of the CSV output
        :return:
        """
        header_not_written = True
        total_output_list = []
        for file1 in os.listdir(full_path_to_csv_file):
            if file1.endswith("csv"):
                filepath = os.path.join(full_path_to_csv_file, file1)
                print("Currently calculating stats for: {}".format(filepath.replace("\\", "/").split("/")[-1]))

                dict_output = self.calc_per_task_for_oneuser(filepath)
                total_output_list.append(dict_output)

                # If the header isn't written yet
                if header_not_written:
                    header_not_written = False
                    with open(csv_output, "w") as file:
                        file.write(",".join(self._header_per_task))
                        file.write("\n")

                with open(csv_output, "a", buffering=4096) as file:
                    for key in dict_output.keys():
                        temp_list = []
                        for key2 in dict_output[key].keys():
                            temp_list.append(dict_output[key][key2])

                        # Should never happen
                        if len(temp_list) != len(self._header_per_task):
                            raise ValueError("Per task headers length does not match with length count of a row!")

                        temp_list = [str(x) for x in temp_list]
                        file.write(",".join(temp_list))
                        file.write("\n")

        print("Finished exporting to {0}".format(csv_output.replace("\\", "/")))


    def calc_per_task_for_oneuser(self, filepath: str):
        """
        Calculate stats per task for one user.
        :param filepath: The absolute path of the file.
        :return A dictionary of the results, with the keys being the tasks
        """
        self._header_per_task = ["ParticipantID", "Task"]
        output_dict = {}
        total_num_fixations = 0
        total_fixation_duration = 0

        with open(filepath, "r") as file:
            pd_dataframe = pd.read_csv(file, index_col=False)

        participant_id = ""
        for char in filepath.replace("\\", "/").split("/")[-1]:
            if char.isdigit():
                participant_id = "".join((participant_id, char))

        task_col = pd_dataframe["Current_task"]
        aoi_col = pd_dataframe["AOI"]

        # # Get the name of the AOIs
        aoi_json_data = utils.load_in_aoi_json()
        temp_data = aoi_json_data["HighBar"]
        aoi_list = []
        for aoi in temp_data.keys():
            s = "_".join((aoi, "AOI"))
            aoi_list.append(s)

        # To store the task that have already been counted
        # NOTE: This is only used as of 2019/04/09 because our data has duplicate tasks
        task_set = set()

        # Store the previous task. The previous task will not have the "appended" name (in case of
        # repeated tasks) in order to preserve the original name of the tasks.
        # For example, if the task is CH5, and the repeated task was named CH52, and prev_task
        # was stored as CH52, then nothing in the original data will match CH52
        prev_task = ""

        # Iterate through all the tasks
        col_length = len(pd_dataframe.index)
        for i in range(col_length):
            cur_task = task_col[i]
            cur_aoi = str(aoi_col[i])
            # Ignore all pretasks and ignore all AOI that are not present
            if cur_task.lower() != "pretask":
                # Only check for duplicate task when a new task is picked up
                if prev_task != cur_task:
                    # Remember to set previous task to unchanged current task!
                    prev_task = cur_task

                    # Change the cur_task to cur_taska, cur_taskb, etc. if cur_task is already in the set
                    if cur_task in task_set:
                        # Iterate through names until a name is not used yet
                        count2 = 0
                        new_name_temp = cur_task
                        while new_name_temp in task_set:
                            new_name_temp = cur_task + chr(ord('a') + count2)
                            count2 += 1
                        cur_task = new_name_temp

                    # Add the current task, whether the name is changed or not, into the task_set
                    task_set.add(cur_task)

                # Initialize the dictionary if it doesn't exist yet
                if cur_task not in output_dict:
                    output_dict[cur_task] = {"ParticipantID": participant_id,
                                             "Task": cur_task,
                                             "TotalNumFixations": 0,
                                             "TotalNumFixationsInAOI": 0,
                                             "TotalProportionsOfFixationsInAOI": 0,
                                             "FixationDuration_Sum": 0,
                                             "FixationDuration_Average": 0,
                                             "FixationDuration_StandardDeviation": [],
                                             "Saccade_length_Sum": 0,
                                             "Saccade_length_Average": 0,
                                             "Saccade_length_StandardDeviation": [],
                                             "Saccade_absolute_angle_Sum": 0,
                                             "Saccade_absolute_angle_Average": 0,
                                             "Saccade_absolute_angle_StandardDeviation": [],
                                             "Saccade_relative_angle_Sum": 0,
                                             "Saccade_relative_angle_Average": 0,
                                             "Saccade_relative_angle_StandardDeviation": []}
                    # Also initialize the AOI columns
                    temp_dict_1 = output_dict[cur_task]
                    for aoi_1 in aoi_list:
                        temp_dict_1[aoi_1 + "_NumberOfFixations"] = 0
                        temp_dict_1[aoi_1 + "_FixationDurationSum"] = 0
                        temp_dict_1[aoi_1 + "_FixationDurationMean"] = 0
                        temp_dict_1[aoi_1 + "_LongestFixationInAOI"] = 0
                        temp_dict_1[aoi_1 + "_ProportionOfTotalFixations"] = 0
                        temp_dict_1[aoi_1 + "_ProportionOFTotalFixationDuration"] = 0

                output_dict[cur_task]["TotalNumFixations"] += 1

                if cur_aoi.lower() != "nan":
                    # Fixation duration
                    cur_fixation_duration = pd_dataframe["FixationDuration"][i].item()
                    total_fixation_duration += cur_fixation_duration

                    cur_saccade_length = pd_dataframe["Saccade_length"][i].item()
                    cur_saccade_abs_angle = abs(pd_dataframe["Saccade_absolute_angle"][i].item())
                    cur_saccade_rel_angle = abs(pd_dataframe["Saccade_relative_angle"][i].item())
                    total_num_fixations += 1

                    # Fixation Duration Sum
                    temp_dict_1 = output_dict[cur_task]
                    temp_dict_1["TotalNumFixationsInAOI"] += 1
                    temp_dict_1["FixationDuration_Sum"] += cur_fixation_duration
                    # Store list for standard deviation calculations later
                    temp_dict_1["FixationDuration_StandardDeviation"].append(cur_fixation_duration)

                    # Saccade Length Sum
                    temp_dict_1["Saccade_length_Sum"] += cur_saccade_length
                    temp_dict_1["Saccade_length_StandardDeviation"].append(cur_saccade_length)

                    # Saccade Absolute Angle Sum
                    temp_dict_1["Saccade_absolute_angle_Sum"] += cur_saccade_abs_angle
                    temp_dict_1["Saccade_absolute_angle_StandardDeviation"].append(cur_saccade_abs_angle)

                    # Saccade Relative Angle Sum
                    temp_dict_1["Saccade_relative_angle_Sum"] += cur_saccade_rel_angle
                    temp_dict_1["Saccade_relative_angle_StandardDeviation"].append(cur_saccade_rel_angle)

                    # Get stats per AOI
                    # Initialize if the AOI doesn't exist yet
                    # aoi_num_fix = "_".join((cur_aoi, "NumberOfFixations"))
                    temp_dict_1 = output_dict[cur_task]
                    temp_dict_1[cur_aoi + "_NumberOfFixations"] += 1
                    temp_dict_1[cur_aoi + "_FixationDurationSum"] += cur_fixation_duration

                    if cur_fixation_duration > temp_dict_1[cur_aoi + "_LongestFixationInAOI"]:
                        temp_dict_1[cur_aoi + "_LongestFixationInAOI"] = cur_fixation_duration

        # +------------------------+
        # | Post stats calculation |
        # +------------------------+
        is_first_time = True
        for cur_task in task_set:
            temp_dict_1 = output_dict[cur_task]
            # Add keys to column headers, but only do it once
            if is_first_time:
                for key in temp_dict_1.keys():
                    if key not in self._header_per_task:
                        self._header_per_task.append(key)

            is_first_time = False
            num_fixations = temp_dict_1["TotalNumFixationsInAOI"]

            # Get standard deviation for fixation duration
            list1 = temp_dict_1["FixationDuration_StandardDeviation"]
            # If the list is empty, set the standard deviation to 0
            temp_dict_1["FixationDuration_StandardDeviation"] = np.std(list1) if list1 else 0

            # Get standard deviation for saccade length
            list1 = temp_dict_1["Saccade_length_StandardDeviation"]
            # If the list is empty, set the standard deviation to 0
            temp_dict_1["Saccade_length_StandardDeviation"] = np.std(list1) if list1 else 0

            # Get standard deviation for saccade absolute angle
            list1 = temp_dict_1["Saccade_absolute_angle_StandardDeviation"]
            # If the list is empty, set the standard deviation to 0
            temp_dict_1["Saccade_absolute_angle_StandardDeviation"] = np.std(list1) if list1 else 0

            # Get standard deviation for saccade relative angle
            list1 = temp_dict_1["Saccade_relative_angle_StandardDeviation"]
            # If the list is empty, set the standard deviation to 0
            temp_dict_1["Saccade_relative_angle_StandardDeviation"] = np.std(list1) if list1 else 0

            if num_fixations != 0:
                # Get average fixation duration
                temp_dict_1["FixationDuration_Average"]  = temp_dict_1["FixationDuration_Sum"] / num_fixations

                # Get average saccade length
                temp_dict_1["Saccade_length_Average"] = temp_dict_1["Saccade_length_Sum"] / num_fixations

                # Get average saccade absolute angle
                temp_dict_1["Saccade_absolute_angle_Average"] = temp_dict_1["Saccade_absolute_angle_Sum"] / num_fixations

                # Get average saccade relative angle
                temp_dict_1["Saccade_relative_angle_Average"] = temp_dict_1["Saccade_relative_angle_Sum"] / num_fixations

                # Now, calculate post-task per AOI
                for aoi in aoi_list:
                    # Get proportion of total fixations
                    aoi_num_fix = temp_dict_1[aoi + "_NumberOfFixations"]
                    temp_dict_1[aoi + "_ProportionOfTotalFixations"] = aoi_num_fix / num_fixations

                    # Get the mean
                    if aoi_num_fix != 0:
                        temp_dict_1[aoi + "_FixationDurationMean"] = temp_dict_1[aoi + "_FixationDurationSum"] / aoi_num_fix

                    # Get proportion of total fixation duration
                    aoi_fix_duration = temp_dict_1[aoi + "_FixationDurationSum"]
                    total_fix_dur_sum = temp_dict_1["FixationDuration_Sum"]
                    if total_fix_dur_sum != 0:
                        temp_dict_1[aoi + "_ProportionOFTotalFixationDuration"] = aoi_fix_duration / total_fix_dur_sum

            # Get proportion of fixations in aoi vs. total fixations
            if temp_dict_1["TotalNumFixations"] != 0:
                temp_dict_1["TotalProportionsOfFixationsInAOI"] = temp_dict_1["TotalNumFixationsInAOI"] / temp_dict_1["TotalNumFixations"]

        return output_dict


    def output_per_task_stats(self, col_headers, dict_input, participant_id, output_dir):
        """
        Output the dictionary into a CSV file.
        :param col_headers: The column headers
        :param dict_input: The dictionary input of the stats
        :param participant_id: The number/ID of the participant.
        :param output_dir: The directory of the output
        :return:
        """
        file_name = "{}_stats.csv".format(participant_id)
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w") as file:
            file.write(",".join(col_headers))
            file.write("\n")

            for task_type in dict_input.keys():
                for aoi in dict_input[task_type].keys():
                    row_list = [participant_id, task_type, aoi]
                    for stats in dict_input[task_type][aoi].keys():
                        row_list.append(str(dict_input[task_type][aoi][stats]))

                    # should never happen
                    if len(row_list) != len(col_headers):
                        raise ValueError("The number of columns in this row does not match the number of column headers.")

                    file.write(",".join(row_list))
                    file.write("\n")

        print("Finished writing to {}".format(file_path.replace("\\", "/")))
