"""
Get the statistical information for all collapsed files and put it into a csv file.
The statistics obtained are:
  1. sum
  2. mean
  3. standard deviation
"""
import pandas as pd
import core.utils as utils
import json


def get_stats(infile, outfile, col_names_list):
    """
    The statistics obtained are:
      1. sum
      2. mean
      3. standard deviation

    # ARGUMENTS
    infile          -> The input csv file.
    outfile         -> The output csv file.
    col_names_list  -> List of column names to obtain stats for.
    """
    df = pd.read_csv(infile, index_col=False)
    return_dict = {}

    basic_stats_dict = {}
    # Get the basic stats
    for col_name in col_names_list:
        temp_dict = {}
        column = df[col_name]
        # sum_key = "".join((col_name, "_sum"))
        # avg_key = "".join((col_name, "_average"))
        # std_key = "".join((col_name, "_std_dev"))

        # Reference for converting from numpy.int64 to native Python types
        # https://stackoverflow.com/a/11389998/6323360
        temp_dict["Sum"] = column.abs().sum().item()
        temp_dict["Average"] = column.abs().mean().item()
        temp_dict["StandardDeviation"] = column.abs().std().item()
        basic_stats_dict[col_name] = temp_dict
    return_dict["BasicStats"] = basic_stats_dict

    # Get the AOI file data
    json_aoi_data = utils.load_in_aoi_json()
    aoi_dict = get_num_fixations_in_aoi(df, json_aoi_data)
    return_dict["AOI"] = aoi_dict
    print(return_dict)

    with open(outfile, "w") as file1:
        json.dump(return_dict, file1, indent=2)

    return return_dict


def get_num_fixations_in_aoi(pd_dataframe, aoi_json_data):
    """
    Get the number of fixations in an AOI.
    :param pd_dataframe: A Pandas dataframe with the read data
    :param aoi_json_file: The AOI Json data
    :rtype A dictionary
    :return Per graph, a dictionary of Fixations per aoi. For example, {"HighBar" : {"Question_AOI": 5}}
    """
    task_col = pd_dataframe["Current_task"]
    graph_col = pd_dataframe["Graph"]
    aoi_col = pd_dataframe["AOI"]
    fixation_duration = pd_dataframe["FixationDuration"]

    graph_type_list = ["HighBar", "LowBar", "HighLine", "LowLine"]
    num_fixation_dict = {}
    for graph_type in graph_type_list:
        temp_data = aoi_json_data[graph_type]
        # Initialize the return dictionary with all number of fixations being 0
        # Reference: https://stackoverflow.com/a/2244026/6323360
        per_aoi_dict = {}
        for key in temp_data.keys():
            key_2 = "_".join((key, "AOI"))
            temp_dict = {}
            temp_dict["NumberOfFixations"] = 0
            temp_dict["FixationDurationSum"] = 0
            temp_dict["FixationDurationMean"] = 0
            per_aoi_dict[key_2] = temp_dict
        num_fixation_dict[graph_type] = per_aoi_dict

    for i in range(len(task_col)):
        cur_task = task_col[i]
        cur_aoi = str(aoi_col[i])
        # Ignore all pretask and ignore all AOI that are empty
        if cur_task.lower() != "pretask".lower() and cur_aoi.lower() != "nan".lower():
            cur_task_graph = list(graph_col[i].lower())
            # Lowercase cur task graph, then uppercase only the first character
            cur_task_graph[0] = cur_task_graph[0].upper()
            cur_task_graph = "".join(cur_task_graph)

            # Current Task Fixation Duration
            cur_task_fixation_duration = fixation_duration[i].item()

            h_or_l = cur_task[1]
            high_or_low = "High" if h_or_l.lower() == "h".lower() else "Low"

            cur_task_key = "".join((high_or_low, cur_task_graph))
            num_fixations_1 = num_fixation_dict[cur_task_key][cur_aoi]["NumberOfFixations"] + 1
            fix_duration_1 = num_fixation_dict[cur_task_key][cur_aoi]["FixationDurationSum"] + cur_task_fixation_duration
            mean_fix_duration_1 = fix_duration_1 / num_fixations_1

            num_fixation_dict[cur_task_key][cur_aoi]["NumberOfFixations"] = round(num_fixations_1, 4)
            num_fixation_dict[cur_task_key][cur_aoi]["FixationDurationSum"] = round(fix_duration_1, 4)
            num_fixation_dict[cur_task_key][cur_aoi]["FixationDurationMean"] = round(mean_fix_duration_1, 4)

    return num_fixation_dict
