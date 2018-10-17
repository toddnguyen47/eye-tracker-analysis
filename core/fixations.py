import pandas as pd

column_names = ["StudyName", "ExportDate", "Name", "Age", "Gender", "StimulusName", "SlideType",
                "EventSource", "UTCTimestamp", "Timestamp", "MediaTime", "TimeSignal", "GazeLeftx",
                "GazeLefty", "GazeRightx", "GazeRighty", "PupilLeft", "PupilRight", "DistanceLeft",
                "DistanceRight", "CameraLeftX", "CameraLeftY", "CameraRightX", "CameraRightY",
                "ValidityLeft", "ValidityRight", "GazeX", "GazeY", "GazeAOI", "InterpolatedGazeX",
                "InterpolatedGazeY", "GazeEventType", "GazeVelocityAngle", "SaccadeSeq", "SaccadeStart",
                "SaccadeDuration", "FixationSeq", "FixationX", "FixationY", "FixationStart",
                "FixationDuration", "FixationAOI", "PostMarker", "Annotation", "LiveMarker", "KeyStroke",
                "MarkerText", "SceneType", "SceneOutput", "SceneParent Current_task"]


def read_in_csv(csv_file):
    # with open(csv_file, "r") as file:
    #     readCSV = csv.reader(file, delimiter=",")
    #     for row in readCSV:
    #         print(row["FixationDuration"])

    # Fill empty columns with -1 for easier parsing
    na_fill_value = -1

    df = pd.read_csv(csv_file, sep=",", header=6, index_col=False)
    df['FixationDuration'] = df['FixationDuration'].fillna(value=na_fill_value)

    # Total number of fixations will be NaN-FixationDuration-NaN
    fixations = df['FixationDuration']

    prev_value = na_fill_value
    fixation_count = 0

    for fixation in fixations:
        if fixation != na_fill_value and fixation != prev_value:
            fixation_count += 1
            prev_value = fixation

    print("Total number of fixations: {}".format(fixation_count))
