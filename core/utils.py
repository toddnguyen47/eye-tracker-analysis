import os
import json


def progress_bar(current, total, elapsed_time, char_to_use="#"):
    """
    Return a string that details the current progress using hashtags.
    """
    import math
    max_hashtag = 30
    num_hashtags = math.floor(current / total * max_hashtag)
    s = ""
    for i in range(num_hashtags):
        s = "".join((s, char_to_use))
    for i in range(max_hashtag - num_hashtags):
        s = "".join((s, " "))

    return_string = "[{}] {:.2%}, {:.2f} seconds collapsed".format(s, current / total, elapsed_time)
    return return_string


def load_in_aoi_json():
    """
    Get the path of the AOI JSON file from params.json, then read in that AOI JSON file and return it in a
    Python dictionary.
    :rtype Python dictionary
    :returns AOI JSON file data
    """
    # Read in the json file
    json_file_path = os.path.join(os.getcwd(), "params.json")
    with open(json_file_path, "r") as file:
        info_filepath = json.load(file)["aoiInfoJson"]

    with open(info_filepath, "r") as file:
        json_aoi_file = json.load(file)

    return json_aoi_file
