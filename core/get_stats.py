import os
import pandas as pd
import core.utils as utils


class GetStats:
    def __init__(self):
        self._header_row_hashset = {}
        self._col_names_list = ["FixationDuration", "Saccade_length", "Saccade_absolute_angle",
                                "Saccade_relative_angle"]


    def get_stats_all_users(self, file_dir, outfile):
        """
        Get stats for all users and put it in the outfile.
        :param file_dir: The file directory
        :param outfile: The outfile to export to a CSV file
        """
        all_stats_list = []
        for (dirpath, dirnames, filenames) in os.walk(file_dir):
            for file in filenames:
                if file.endswith("csv"):
                    print("Calculating stats for file {}...".format(file))
                    filepath = os.path.join(dirpath, file)
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
        dict1 = {}

        task_col = pd_dataframe["Current_task"]
        graph_col = pd_dataframe["Graph"]
        aoi_col = pd_dataframe["AOI"]
        fixation_duration = pd_dataframe["FixationDuration"]

        temp_data = aoi_json_data["HighBar"]
        temp_data["NoAOI"] = None
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

        total_num_fixations = 0
        total_fixation_duration = 0

        for i in range(len(task_col)):
            cur_task = task_col[i]
            cur_aoi = str(aoi_col[i])
            # Ignore all pretask
            if cur_task.lower() != "pretask".lower():
                total_num_fixations += 1
                # Ignore all fixations that are not in AOI
                if cur_aoi.lower() == "nan".lower():
                    cur_aoi = "NoAOI_AOI"

                cur_task_graph = list(graph_col[i].lower())
                # Lowercase cur task graph, then uppercase only the first character
                cur_task_graph[0] = cur_task_graph[0].upper()
                cur_task_graph = "".join(cur_task_graph)

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
            proportionKey = "_ProportionOfTotalFixations"
            if total_num_fixations == 0:
                dict1[key + proportionKey] = 0
            else:
                proportionValue = dict1[key + "_NumberOfFixations"] / total_num_fixations
                proportionValue = round(proportionValue, 6)
                dict1[key + proportionKey] = proportionValue

            # Get the proportion of total number of fixation duration
            proportionKey = "_ProportionOfTotalFixationDuration"
            if total_fixation_duration == 0:
                dict1[key + proportionKey] = 0
            else:
                proportionValue = dict1[key + "_FixationDurationSum"] / total_fixation_duration
                proportionValue = round(proportionValue, 6)
                dict1[key + proportionKey] = proportionValue

        # Add keys to list, then add values to return list
        return_list = []
        for key in dict1.keys():
            self._header_row_hashset[key] = None
            return_list.append(str(dict1[key]))

        return return_list
