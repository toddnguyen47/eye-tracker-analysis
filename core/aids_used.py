import pandas as pd
import os

class AidsUsed:
    def __init__(self, aids_used_filepath, aoi_files_dir, output_filedir):
        self.aids_used_filepath = aids_used_filepath
        self.aoi_files_dir = aoi_files_dir
        self.output_filedir = output_filedir

    def read_in_aids_used(self) -> dict:
        """
        Read in the aids used file.
        :return: A dictionary consisting of "FirstName LastName TaskID" as the key, and the Aids_Used (Yes/No) as the values.
        """
        df = pd.read_csv(self.aids_used_filepath, index_col=False)

        return_dict = {}

        # For each line read
        for index, row in df.iterrows():
            last_name = row["LastName"]
            first_name = row["FirstName"]
            task_id = row["TaskID"]
            aids_used = int(row["Aids used (Binary)"])

            aids_used_str = "No"
            if aids_used == 1:
                aids_used_str = "Yes"

            key = "{0} {1} {2}".format(first_name, last_name, task_id)
            return_dict[key] = aids_used_str

        return return_dict

    def merge_aids_used(self):
        """
        Merge the aids used with the AOI file.
        :return:
        """
        aids_used_dict = self.read_in_aids_used()

        # For each file in the
        for file in os.listdir(self.aoi_files_dir):
            if file.endswith("csv"):
                full_filepath = os.path.join(self.aoi_files_dir, file)
                df = pd.read_csv(full_filepath, index_col=False)

                aids_used_list = []
                # For each row
                for index, row in df.iterrows():
                    full_name = row["Name"].strip().replace('\'', "")
                    task_id = row["Current_task"]

                    # If not pretask
                    if str(task_id).lower() != "pretask".lower():
                        key = "{0} {1}".format(full_name, task_id)
                        aids_used = aids_used_dict[key]
                        aids_used_list.append(aids_used)
                    # If pretask, append an empty string
                    else:
                        aids_used_list.append("")

                df["Aids_Used"] = aids_used_list

                # get a new filename
                new_filename = file.split(".")[:-1]
                new_filename.append("_AidsUsed.csv")
                new_filename = "".join(new_filename)

                new_file_fullpath = os.path.join(self.output_filedir, new_filename)
                print("Exporting to {0}".format(new_file_fullpath[-45:]))
                df.to_csv(new_file_fullpath)

        print("Finished!")
