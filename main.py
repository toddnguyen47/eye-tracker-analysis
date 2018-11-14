# import EMDAT_src
import core.fixations as fixations
import core.calculations as calculations
import core.label_graphs as label_graphs
import params
import sys

valid_arguments = ["fixation_collapse", "label_graphs", "saccade_calc"]


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
    else:
        print("Invalid command line argument.")
        print_commands()
