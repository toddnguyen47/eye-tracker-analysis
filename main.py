# import EMDAT_src
import core.fixations as fixations
import core.calculations as calculations
import core.label_graphs as label_graphs
from core.get_stats import GetStats
from core.area_of_interest import AreaOfInterest
from core.aids_used import AidsUsed
import argparse
import sys
import json

valid_commands = ["fixation_collapse", "label_graphs", "saccade_calc", "stats_calc",
                  "aoi_calc", "aids_used_calc"]

# Load in the params.json file
with open("params.json", "r") as file:
    json_data = json.load(file)


# Start the command line arguments
s = "Various functions to calculate things relating to eye gaze, such as saccade calculations or\n\
Area of Interest (AOI) calculation. The valid commands are:\n\
{}".format(", ".join(valid_commands))
parser = argparse.ArgumentParser(description=s, formatter_class=argparse.RawDescriptionHelpFormatter)

# help_str_2 = ", ".join(valid_commands)
# help_str = "Various commands that can be done with this program. Correct commands are: {}".format(help_str_2)
# parser.add_argument("command", metavar="command", help=help_str, choices=valid_commands)

subparsers = parser.add_subparsers(title="Valid commands", description="For additional help with \
these commands, type into the terminal:\n\
    python main.py command_name -h\n\
For example,\n\
    python main.py {} -h".format(valid_commands[0]), dest="command_name")

# Create parser for the fixation_collapse command
parser_fixation_collapse = subparsers.add_parser(valid_commands[0], help="Collapse a fixation file \
    into a smaller fixation file with one fixation per line")
parser_fixation_collapse.add_argument("init_fixation_file", help="The path to the initial fixation file",
    metavar="init_file")
parser_fixation_collapse.add_argument("collapsed_fixation_file", help="The path to the smaller, \
    collapsed fixation file", metavar="collapsed_file")

# Create parser for the label graphs command
parser_label_graphs = subparsers.add_parser(valid_commands[1], help="Label the graphs from the \
    completion time file. The completion file path can be found in params.json")
parser_label_graphs.add_argument("collapsed_fixation_file", help="The path to the collapsed fixation file.",
    metavar="collapsed_file")

# Create parser for the saccade calculation command
parser_saccade_calc = subparsers.add_parser(valid_commands[2], help="Calculate saccades based on \
    the fixations")
parser_saccade_calc.add_argument("collapsed_fixation_file", help="The path to the collapsed fixation file.",
    metavar="collapsed_file")

# Create parser for the statistics calculation command
parser_stats_calc = subparsers.add_parser(valid_commands[3], help="Calculate statistics, including \
    mean, median, standard deviation, and many more.")
parser_stats_calc.add_argument("user_or_task", help="Denote whether you want to calculate the statistics \
    of all users, or per task for one user.", choices=["all_users", "per_task"])
parser_stats_calc.add_argument("file_directory", help="The path to the collapsed fixation file directory.")
parser_stats_calc.add_argument("output", help="The csv file to output the stats to. NOTE that this will \
                                              be overwritten!")

# Create parser for the AOI calculations command
parser_aoi_calc = subparsers.add_parser(valid_commands[4], help="Calculate whether the fixations \
    are in a certain Area of Interest (AOI) and if it is in an AOI, note which AOI that fixation \
    belongs to.")
parser_aoi_calc.add_argument("file_directory", help="The directory where the collapsed CSV files \
    are stored.")

# Create parser for the aids used command
parser_aids_used = subparsers.add_parser(valid_commands[5], help="Combine information from the AIDS used CSV file \
    and the AOI file into one CSV file.")
parser_aids_used.add_argument("aids_used_filepath", help="The full path to the aids used file.")
parser_aids_used.add_argument("file_directory", help="The directory where the collapsed CSV files \
    are stored.")
parser_aids_used.add_argument("output_directory", help="The directory of where the output files will be.")

# Compile all the command line parser and subparsers
args = parser.parse_args()

# If no outputs are supplied, print help
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

# Handle Fixation Collapse
if args.command_name == valid_commands[0]:
    fixations.collapse_to_fixations(args.init_fixation_file, args.collapsed_fixation_file)

# Handle Labeling Graphs using the Completion Time CSV
elif args.command_name == valid_commands[1]:
    label_graphs.label_graphs(args.collapsed_fixation_file, json_data["completionTimeCsv"])

# Handle Saccade calculation
elif args.command_name == valid_commands[2]:
    calculations.calculate(args.collapsed_fixation_file)

# Handle statistics calculation
elif args.command_name == valid_commands[3]:
    get_stats_obj = GetStats()
    # Handle all users stats calculation
    if args.user_or_task == "all_users":
        get_stats_obj.get_stats_all_users(args.file_directory, args.output)
    # Handle per task per user calculation
    elif args.user_or_task == "per_task":
        get_stats_obj.get_stats_per_task(args.file_directory, args.output)

# Handle AOI calculation
elif args.command_name == valid_commands[4]:
    aoi_obj = AreaOfInterest()
    aoi_obj.execute(args.file_directory)

# Handle Aids used merging
elif args.command_name == valid_commands[5]:
    aids_used_obj = AidsUsed(
        aids_used_filepath=args.aids_used_filepath,
        aoi_files_dir=args.file_directory,
        output_filedir=args.output_directory
    )
    aids_used_obj.merge_aids_used_no_aids()
