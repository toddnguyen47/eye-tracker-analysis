import pandas as pd
import params
import math


def read_in_file(filename):
    """
    Read in a collapsed file, then add the corresponding label from params.GRAPH_INFO_FILE

    # ARGUMENTS
    filename    -> The name of the CSV file.
    """
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
            graph_temp = graph_row["graph"].values[0]
        graph_list.append(graph_temp)
    
    # Add the row "Graph" back into the dataframe
    df['Graph'] = graph_list

    new_filename = "".join((filename.split(".csv")[0], "_graphlabel.csv"))
    df.to_csv(new_filename, index=False)
    print("Finished exporting to {}".format(new_filename))
