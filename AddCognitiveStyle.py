import pandas as pd
from abc import ABC, abstractmethod
import os


class AbstractBaseClass(ABC):
    """
    Abstract Base Class to use for our screens.
    """

    @abstractmethod
    def execute(self):
        print("")
        print("CURRENT SCREEN: " + self.class_name)

    def __init__(
            self,
            class_name: str,
            next_screen: "AbstractBaseClass" = None,
            prev_screen: "AbstractBaseClass" = None,
            default_screen: "AbstractBaseClass" = None,
    ):
        """
        Constructor that requires a next class and a previous class.

        :param class_name: The class name to display.
        :param next_screen: The next state.
        :param prev_screen: The previous state.
        :param default_screen: The default screen to return to.
        """
        super(AbstractBaseClass, self).__init__()

        self.next_screen: AbstractBaseClass = next_screen
        self.prev_screen: AbstractBaseClass = prev_screen
        self.default_screen: AbstractBaseClass = default_screen
        self.class_name = class_name

    def get_high_med_low(self, str_input: str) -> str:
        """
        Convert 3 to High, 2 to Medium, and 1 to low.
        :param str_input: The string input.
        :return: "High", "Medium", or "Low"
        """
        int_i = int(str_input)
        if int_i == 3:
            str1 = "High"
        elif int_i == 2:
            str1 = "Medium"
        elif int_i == 1:
            str1 = "Low"
        else:
            raise ValueError("not 3, 2, or 1")

        return str1

    def get_high_low(self, str_input: str) -> str:
        """
        Convert 1 to "High" and 0 to "Low"
        :param str_input: The string input.
        :return: "High", "Medium", or "Low"
        """
        int_i = int(str_input)
        if int_i == 1:
            str1 = "High"
        elif int_i == 0:
            str1 = "Low"
        else:
            raise ValueError("not 3, 2, or 1")

        return str1

    def get_dict_of_participants(self) -> dict:
        """
        Get the dictionary of participants, with participant ID being the key and the values is a list of
        [hi/me/lo, hi/lo] values.

        :return: Dictionary of participants
        """

        print("Enter path of Cognitive Style with ID CSV file:")
        cognitive_style_csv = input(">>> ")

        cog_df = pd.read_csv(cognitive_style_csv, index_col=False)
        dict_of_participants = {}
        for index, row in cog_df.iterrows():
            participant_id = row["ParticipantID"]
            if participant_id != 0:
                himelo = self.get_high_med_low(row["HIGH-3/MEDIUM-2/LOW-1"])
                hilo = self.get_high_low(row["HIGH-1/LOW-0"])
                dict_of_participants[participant_id] = [himelo, hilo]

        return dict_of_participants


class MainScreen(AbstractBaseClass):
    def __init__(self):
        super(MainScreen, self).__init__("Main Screen")
        self.default_screen = self

    def execute(self):
        """
        Main execute function
        """
        super().execute()
        print("Select option by typing in a number, e.g. 1")
        print("[1] Add Name to Cognitive Style CSV")
        print("[2] All Users")
        print("[3] Per Task")
        print("[-1] Quit")
        user_input = input(">>> ")

        # Handle adding names to cognitive style CSV
        if "1" == user_input:
            return AddNameToCogStyleCsv()

        # Handle all users
        elif "2" == user_input:
            return AllUsers()

        # Handle per task
        elif "3" == user_input:
            print("Per Task")

        elif "-1" == user_input:
            return None

        # Exit
        else:
            print("No option matches your option. Returning to main screen.")
            return self.default_screen


class AddNameToCogStyleCsv(AbstractBaseClass):
    def __init__(self):
        super(AddNameToCogStyleCsv, self).__init__("Add Name to Cognitive Style CSV")
        self.default_screen = MainScreen()

    def execute(self):
        print("Enter the path for the Cognitive Style CSV, or enter -1 to return to the main screen.")
        cognitive_style_csv_filepath = input(">>> ")

        if "-1" != cognitive_style_csv_filepath:
            self.add_name_to_cogstyle(cognitive_style_csv_filepath)
            print("Finished!")

        return self.default_screen

    def add_name_to_cogstyle(self, cognitive_style_csv_filepath: str):
        cogstyle_df = pd.read_csv(cognitive_style_csv_filepath, index_col=False)

        print("Enter the path for the directory of the Collapsed_with_AOI CSV files.")
        filepath = input(">>> ")
        participant_id_list = [0] * len(cogstyle_df.index)

        for file in os.listdir(filepath):
            if file.endswith("csv"):
                participant_id = ""
                for char in file:
                    if char.isdigit():
                        participant_id = "".join((participant_id, char))

                participant_id = int(participant_id)

                full_fp = os.path.join(filepath, file)
                df = pd.read_csv(full_fp, index_col=False)
                name = df["Name"][0].split(" ")
                last_name = name[1]
                first_name = name[0]

                lastname_df = cogstyle_df["LastName"]
                # Iterate through all last names
                for i in range(len(lastname_df)):
                    name2 = lastname_df[i]
                    if (name2 == last_name) and (first_name == cogstyle_df["FirstName"][i]):
                        participant_id_list[i] = participant_id

        cogstyle_df["ParticipantID"] = participant_id_list
        cogstyle_df.to_csv("CognitiveStyleWithID.csv", index=False)

        print("Exported to CognitiveStyleWithID.csv")


class AllUsers(AbstractBaseClass):
    def __init__(self):
        super(AllUsers, self).__init__("All Users")
        self.default_screen = MainScreen()
        self.dict_of_participants = self.get_dict_of_participants()

    def execute(self):
        super().execute()

        print("Enter path of the stats CSV file, or -1 to return to main screen.")
        print("Please be aware that your CSV file will be overwritten.")
        user_input = input(">>> ")

        if "-1" != user_input:
            self.convert_cogtype_all_users(user_input)
            print("Finished!")

        return self.default_screen

    def convert_cogtype_all_users(self, path_to_csv: str):
        """
        Convert cognitive type to HIGH / MEDIUM / LOW

        :param path_to_csv: The path of the stats CSV file.
        """
        df_all_users = pd.read_csv(path_to_csv, index_col=False)

        hi_md_lo_list = []
        hi_lo_list = []
        dict_of_participants = self.get_dict_of_participants()

        for index, row in df_all_users.iterrows():
            participant_id = row["Participant"]
            cogstyle = dict_of_participants[participant_id]
            hi_md_lo_list.append(cogstyle[0])
            hi_lo_list.append(cogstyle[1])

        df_all_users["HIGH-3/MEDIUM-2/LOW-1"] = hi_md_lo_list
        df_all_users["HIGH-1/LOW-0"] = hi_lo_list
        df_all_users.to_csv("statsAllUsersCogStyle.csv", index=False)

        print("Exported to statsAllUsersCogStyle.csv")


class PerTask(AbstractBaseClass):
    def __init__(self):
        super(PerTask, self).__init__("Per Task")
        self.default_screen = MainScreen()

    def execute(self):
        super().execute()

        print("Enter path of the stats CSV file, or -1 to return to main screen.")
        print("Please be aware that your CSV file will be overwritten.")
        user_input = input(">>> ")

        if "-1" != user_input:
            self.convert_cogtype_per_task(user_input)
            print("Finished!")

        return self.default_screen

    def convert_cogtype_per_task(self, path_to_csv: str):
        """
        Convert cognitive style to HIGH / LOW

        :param path_to_csv: Path to the Stats CSV file
        """
        df_per_task = pd.read_csv(path_to_csv, index_col=False)
        hi_md_lo_list = []
        hi_lo_list = []
        dict_of_participants = self.get_dict_of_participants()

        for index, row in df_per_task.iterrows():
            participant_id = row["ParticipantID"]
            cogstyle = dict_of_participants[participant_id]
            hi_md_lo_list.append(cogstyle[0])
            hi_lo_list.append(cogstyle[1])

        df_per_task["HIGH-3/MEDIUM-2/LOW-1"] = hi_md_lo_list
        df_per_task["HIGH-1/LOW-0"] = hi_lo_list
        df_per_task.to_csv("statsPerTaskCogStyle.csv", index=False)

        print("Exported to statsPerTaskCogStyle.csv")


if __name__ == "__main__":
    current_screen = MainScreen()
    while True:
        current_screen = current_screen.execute()

        if None is current_screen:
            break

    print("Thank you for using this software!")
