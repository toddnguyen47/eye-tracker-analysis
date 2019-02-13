"""
Get the statistical information for all collapsed files and put it into a csv file.
The statistics obtained are:
  1. sum
  2. mean
  3. standard deviation
"""
import pandas as pd


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
    return_list = []

    for col_name in col_names_list:
        temp_dict = {}
        column = df[col_name]
        sum_key = "".join((col_name, "_sum"))
        avg_key = "".join((col_name, "_average"))
        std_key = "".join((col_name, "_std_dev"))

        temp_dict[sum_key] = column.abs().sum()
        temp_dict[avg_key] = column.abs().mean()
        temp_dict[std_key] = column.abs().std()
        return_list.append(temp_dict)

    print(return_list)
    return return_list
