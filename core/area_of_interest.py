"""
Various functions relating to areas of interests (AOI).
"""
import pandas as pd
import os
import core.utils as utils


class AreaOfInterest:
    def __init__(self):
        # Read in the json file
        self._aoi_file = utils.load_in_aoi_json()

        # Only ask user once if it is okay to overwrite
        self._output_aoi_path_exists_first_time = True


    def execute(self, input_file_dir):
        """
        Read in csv file/files in input_file_dir, and add 5 AOI columns: aoi_topleft_x, aoi_topleft_y,
        aoi_width, aoi_height, and is_saccade_within_aoi.

        :params input_file_dir: A file or file directory to add the 5 AOI columns to.
        """
        # If input_file_dir is a file
        if os.path.isfile(input_file_dir):
            self.add_aoi_to_csv(input_file_dir)
        # Else, if input_file_dir is a file directory
        else:
            for subdir, dirs, files in os.walk(input_file_dir):
                for file in files:
                    if file.endswith(".csv"):
                        full_path = os.path.join(subdir, file)
                        self.add_aoi_to_csv(csv_file=full_path)


    def add_aoi_to_csv(self, csv_file):
        """
        For each fixation, check if it's in any of the Area of Interests. If it is, add the
        TYPE of area of interest that that fixation is in. For example, if a fixation is
        in the Question AOI, the column will display "Question AOI".

        :param csv_file: The CSV file to look for Areas of Interest.
        """
        csv_df = pd.read_csv(csv_file, index_col=False)
        aoi_type_list = []

        for index, row in csv_df.iterrows():
            cur_task = row["Current_task"]
            aoi_type = ""

            # Ignore all pretask and fill in None values for pretask
            if cur_task.lower() != "pretask".lower():
                fixation_x = row["FixationX"]
                fixation_y = row["FixationY"]

                low_or_high = cur_task[1]
                low_or_high = "High" if low_or_high.upper() == "H" else "Low"

                # Make only the first character uppercase
                graph_type = list(row["Graph"].lower())
                graph_type[0] = graph_type[0].upper()
                graph_type = "".join(graph_type)

                graph_type = "".join((low_or_high, graph_type))

                graph_type_dict = self._aoi_file[graph_type]
                # For each AOI in the graph type dict
                for aoi_type_temp in graph_type_dict.keys():
                    coords_list = graph_type_dict[aoi_type_temp]
                    top_left = [int(x) for x in coords_list[0].split(",")]
                    bot_left = [int(x) for x in coords_list[1].split(",")]
                    top_right = [int(x) for x in coords_list[2].split(",")]
                    bot_right = [int(x) for x in coords_list[3].split(",")]
                    if self.check_if_saccade_in_aoi_coords(fixation_x=fixation_x, fixation_y=fixation_y,
                        aoi_topleft=top_left, aoi_botleft=bot_left, aoi_topright=top_right, aoi_botright=bot_right):
                        # If the saccade is in the AOI, put the AOI type into the list
                        aoi_type = "".join((aoi_type_temp, "_AOI"))
                        break
            aoi_type_list.append(aoi_type)

        csv_df["AOI"] = aoi_type_list
        temp_list = csv_file.split("\\")
        csv_filename = temp_list[-1]
        parent_folder = temp_list[-2]

        path_before = csv_file[:-(len(csv_filename) + len("/") + len(parent_folder) + len("/"))]
        csv_path_collapsed_aoi = os.path.join(path_before, "CollapsedWithAOI")

        if self._output_aoi_path_exists_first_time:
            self._output_aoi_path_exists_first_time = False

            # If directory exists, ask user if we want to overwrite csv files
            if os.path.isdir(csv_path_collapsed_aoi):
                print("{0} exists, which means CSV files might exist in here.".format(csv_path_collapsed_aoi.replace("\\", "/")))
                print("Is it okay to overwrite these CSV files? (Y/N)")
                yes_or_no = input(">>> ")

                # If no, exit
                if yes_or_no.lower() == "n":
                    print("Exiting program...")
                    import sys
                    sys.exit()

            # Create directory if directory doesn't exist
            else:
                os.mkdir(csv_path_collapsed_aoi)

        csv_file_output = os.path.join(csv_path_collapsed_aoi, csv_filename)
        csv_df.to_csv(csv_file_output, index=None)
        print("Finished exporting to {}".format(csv_file_output.replace("\\", "/")))


    def check_if_saccade_in_aoi_coords(self, fixation_x, fixation_y,
        aoi_topleft, aoi_botleft, aoi_topright, aoi_botright):
        """
        Check if the saccade is in the Area of Interest using the top left, bot left, top right,
        and bot right coordinates.

        :param fixation_x: Saccade's x-coordinate
        :param fixation_y: Saccade's y-coordinate
        :param aoi_topleft: Area of Interest's top left coordinates
        :param aoi_botleft: Area of Interest's bottom left coordinates.
        :param aoi_topright: Area of Interest's top right coordinates.
        :param aoi_botright: Area of Interest's bot right coordinates.
        """
        left_x = aoi_topleft[0]
        right_x = aoi_botright[0]
        top_y = aoi_topleft[1]
        bot_y = aoi_botright[1]

        # Check if the saccade x coordinates are within the aoi
        fixation_within_x = left_x <= fixation_x <= right_x
        if not fixation_within_x:
            return False

        # Check if the saccade y coordinates are within the aoi
        fixation_within_y = top_y <= fixation_y <= bot_y
        if not fixation_within_y:
            return False

        return fixation_within_x and fixation_within_y


    def check_if_saccade_in_aoi(self, fixation_x, fixation_y, aoi_x, aoi_y,
                                aoi_width, aoi_height):
        """
        Check if the saccade is in the Area of Interest using width and height.

        :param fixation_x: Saccade's x-coordinate
        :param fixation_y: Saccade's y-coordinate
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
        fixation_within_x = left_x <= fixation_x <= right_x
        if not fixation_within_x:
            return False

        # Check if the saccade y coordinates are within the aoi
        fixation_within_y = top_y <= fixation_y <= bot_y
        if not fixation_within_y:
            return False

        return fixation_within_x and fixation_within_y
