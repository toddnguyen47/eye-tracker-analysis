import pandas as pd
import params
import math
import os


def label_graphs(filename):
    """
    Read in a collapsed file, then add the corresponding label from params.GRAPH_INFO_FILE

    # ARGUMENTS
    filename    -> The name of the CSV file.
    """
    overwrite = "y"
    # If output file exists
    if (os.path.exists(filename)):
        overwrite = input("File \"{}\" exists. Would you like to overwrite? (Y/N): "
                          .format(filename).replace("\\", "/"))

    if overwrite.strip().lower() == "y":
        df = pd.read_csv(filename, index_col=False)

        # Find the name column
        name = df['Name'][0].split(" ")
        first_name = name[0]
        last_name = name[1]
        
        # Read in data from params.GRAPH_INFO_FILE and make a smaller dataframe
        # based on first_name and last_name
        graph_label_df = pd.read_csv(params.GRAPH_INFO_FILE, index_col=False)
        name_based_df = pd.DataFrame(columns=graph_label_df.columns)
        for index, row in graph_label_df.iterrows():
            cur_first_name = row['FirstName']
            cur_last_name = row['LastName']
            if cur_first_name == first_name and cur_last_name == last_name:
                name_df_len = len(name_based_df.index)
                name_based_df.loc[name_df_len] = row

        # Now we iterate through the collapsed file and find our desired information
        # in the smaller dataframe obtained above
        graph_list = []
        for index, row in df.iterrows():
            cur_task = row['Current_task']
            graph_temp = math.nan
            # ignore all pretest data
            if cur_task.lower() != "pretask":
                # find the current task in the smaller dataframe
                graph_row = name_based_df[name_based_df["TaskID"].str.contains(cur_task)]
                try:
                    graph_temp = graph_row["graph"].values[0]
                except IndexError as error:
                    # print(error)
                    raise IndexError("Please make sure the participant's First and Last Name is correctly formatted. The format should be \"FirstName LastName\", e.g. \"Jane Lastnameton\"")
            graph_list.append(graph_temp)
        
        # Add the row "Graph" back into the dataframe
        df['Graph'] = graph_list

        df.to_csv(filename, index=False)
        print("Finished exporting to {}".format(filename).replace("\\", "/"))

    else:
        print("Exiting...")
