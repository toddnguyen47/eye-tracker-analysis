"""
Various functions relating to areas of interests (AOI).
"""
import pandas as pd
import params
import os


class AreaOfInterest:
    def __init__(self):
        pass

    def execute(self, file_directory):
        """
        WARNING: This function WILL overwrite any existing CSV files. Make sure you have adequate backup files
        before executing this function!

        Read in csv file/files in file_directory, and add 5 AOI columns: aoi_topleft_x, aoi_topleft_y,
        aoi_width, aoi_height, and is_saccade_within_aoi.

        :params file_directory: A file or file directory to add the 5 AOI columns to.
        """
        # If file_directory is a file
        if os.path.isfile(file_directory):
            self.add_aoi_to_csv(file_directory)
        # Else, if file_directory is a file directory
        else:
            for subdir, dirs, files in os.walk(file_directory):
                for file in files:
                    if file.endswith(".csv"):
                        full_path = os.path.join(subdir, file)
                        self.add_aoi_to_csv(csv_file=full_path)


    def add_aoi_to_csv(self, csv_file):
        """
        Read in a csv_file and outputs to that same csv_file 5 added AOI columns: aoi_topleft_x, aoi_topleft_y,
        aoi_width, aoi_height, and is_saccade_within_aoi.

        NOTE: There is NO warning that the csv_file will be erased! Be careful!
        :params csv_file: The csv_file to read and overwrite.
        """
        aoi_dict = self.build_aoi_dict()
        aoi_topleft_x_list = []
        aoi_topleft_y_list = []
        aoi_width_list = []
        aoi_height_list = []
        within_aoi_list = []

        df = pd.read_csv(csv_file, index_col=None)
        for index, row in df.iterrows():
            cur_task = row["Current_task"]
            # Ignore all pretask and fill in None values for pretask
            if cur_task.lower() != "pretask".lower():
                low_or_high = cur_task[1]
                low_or_high = "high" if low_or_high.upper() == "H" else "low"

                # Make only the first character uppercase
                graph_type = list(row["Graph"].lower())
                graph_type[0] = graph_type[0].upper()
                graph_type = "".join(graph_type)

                task_name = low_or_high + graph_type
                aoi_info = aoi_dict[task_name]
                aoi_x = aoi_info[0]
                aoi_y = aoi_info[1]
                aoi_width = aoi_info[2]
                aoi_height = aoi_info[3]
                saccade_x = row["FixationX"]
                saccade_y = row["FixationY"]

                is_saccade_within_aoi = self.check_if_saccade_in_aoi(saccade_x=saccade_x, saccade_y=saccade_y, aoi_x=aoi_x,
                    aoi_y=aoi_y, aoi_width=aoi_width, aoi_height=aoi_height)

                aoi_topleft_x_list.append(aoi_x)
                aoi_topleft_y_list.append(aoi_y)
                aoi_width_list.append(aoi_width)
                aoi_height_list.append(aoi_height)
                within_aoi_list.append(is_saccade_within_aoi)

            # Fill out None values for pretask
            else:
                aoi_topleft_x_list.append(None)
                aoi_topleft_y_list.append(None)
                aoi_width_list.append(None)
                aoi_height_list.append(None)
                within_aoi_list.append(None)

        # Add the rows back into the dataframes
        df["AOITopLeftX"] = aoi_topleft_x_list
        df["AOITopLeftY"] = aoi_topleft_y_list
        df["AOIWidth"] = aoi_width_list
        df["AOIHeight"] = aoi_height_list
        df["SaccadeWithinAOI"] = within_aoi_list

        df.to_csv(csv_file, index=None)
        print("Finished exporting to {}".format(csv_file.replace("\\", "/")))


    def build_aoi_dict(self):
        """
        Build an area of interest dictionary based on the screenshots.

        :returns A dictionary with taskName as the key, and [aoi_x, aoi_y, aoi_width, aoi_height]
        as values
        """
        df = pd.read_csv(params.AOI_INFO, index_col=None)
        dict1 = {}

        for index, row in df.iterrows():
            task_name = row["TaskName"]
            aoi_top_left = row["TopLeftCoordinates"].split(",")
            aoi_x = int(aoi_top_left[0])
            aoi_y = int(aoi_top_left[1])
            aoi_width = row["Width"]
            aoi_height = row["Height"]
            dict1[task_name] = [aoi_x, aoi_y, aoi_width, aoi_height]

        return dict1


    def check_if_saccade_in_aoi(self, saccade_x, saccade_y, aoi_x, aoi_y,
                                aoi_width, aoi_height):
        """
        Check if the saccade is in the Area of Interest.

        :param saccade_x: Saccade's x-coordinate
        :param saccade_y: Saccade's y-coordinate
        :param aoi_x: Area of Interest's x-coordinate
        :param aoi_y: Area of Interest's y-coordinate
        :param aoi_width: Area of Interest's width
        :param aoi_height: Area of Interest's height
        """
        # The area of interest has 4 values:
        # left_x: aoi_x
        # right_x: aoi_x + aoi_width
        # top_y: aoi_y
        # bot_y: aoi_y + aoi_height
        left_x = aoi_x
        right_x = aoi_x + aoi_width
        top_y = aoi_y
        bot_y = aoi_y + aoi_height

        # Check if the saccade x coordinates are within the aoi
        saccade_within_x = left_x <= saccade_x <= right_x
        if not saccade_within_x:
            return False

        # Check if the saccade y coordinates are within the aoi
        saccade_within_y = top_y <= saccade_y <= bot_y
        if not saccade_within_y:
            return False

        return saccade_within_x and saccade_within_y
