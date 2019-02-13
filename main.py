# import EMDAT_src
import core.fixations as fixations
import core.calculations as calculations
import core.label_graphs as label_graphs
import core.get_stats as get_stats
from core.area_of_interest import AreaOfInterest
import params

valid_arguments = ["fixation_collapse", "label_graphs", "saccade_calc", "stats_calc",
                   "aoi_calc"]


def print_commands():
    print("You can type just the number or the full option name. Valid options are:")
    count = 1
    for arg in valid_arguments:
        print("  [{}] {}".format(count, arg))
        count += 1
    print("")


if __name__ == "__main__":
    print_commands()
    argument = input(">>> ")
    # collapse argument
    if argument == "1" or argument == valid_arguments[0]:
        fixations.collapse_to_fixations(params.INPUT_CSV_FILENAME)
    # label graphs
    elif argument == "2" or argument == valid_arguments[1]:
        label_graphs.label_graphs(params.COLLAPSED_CSV_FILENAME)
    # saccade_calc
    elif argument == "3" or argument == valid_arguments[2]:
        calculations.calculate(params.COLLAPSED_CSV_FILENAME)
    # calculate stats
    elif argument == "4" or argument == valid_arguments[3]:
        columns_to_obtain = ["Saccade_length", "Saccade_absolute_angle", "Saccade_relative_angle"]
        get_stats.get_stats(infile=params.COLLAPSED_CSV_FILENAME, outfile=None,
                            col_names_list=columns_to_obtain)
    # AOI calculations
    elif argument == "5" or argument == valid_arguments[4]:
        aoi_obj = AreaOfInterest()
        aoi_obj.execute(params.COLLAPSED_CSV_FILE_DIRECTORY)
    else:
        print("Invalid command line argument.")
        print_commands()
