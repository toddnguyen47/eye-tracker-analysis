# import EMDAT_src
import core.fixations as fixations
import params
import sys

valid_arguments = ["collapse", "saccade_calc"]


def print_error():
    print("Valid command line options are:")
    for arg in valid_arguments:
        print(">>> {}".format(arg))


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Please provide a command line argument.")
        print_error()
    else:
        argument = sys.argv[1].strip().lower()
        # collapse argument
        if argument == valid_arguments[0]:
            fixations.collapse_to_fixations(params.INPUT_CSV_FILENAME)
        # saccade_calc
        elif argument == valid_arguments[1]:
            fixations.get_saccade_length(params.INPUT_CSV_FILENAME)
        else:
            print("Invalid command line argument.")
            print_error()