import os
import csv

class Setting:

    DEFAULT_LEARN_RATE = 0.1
    DEFAULT_MAX_ITERATIONS = 100_000
    DEFAULT_SAMPLE_SIZE = 50

    def __init__(self, mode: str, dependent_feature: str, separator: str) -> None:
        self.separator = separator
        self.dependent_feature = dependent_feature
        self.mode = mode

    def get_dependent_feature(self) -> str:
        return self.dependent_feature

    def set_dependent_feature(self, dependent_feature: str) -> None:
        self.dependent_feature = dependent_feature

    def get_mode(self) -> str:
        return self.mode

    def set_mode(self, mode: str) -> None:
        self.mode = mode
    
    def get_setting_list(self) -> list[str]:
        return [self.mode, self.dependent_feature, self.separator] 

def save_settings(settings: str, project_name: str) -> None:
    path = os.path.join(
        os.path.dirname(__file__),
        "projects",
        project_name,
        f"{project_name}_setting.csv"
    )

    with open(path,"w") as file:
        for setting in settings.get_setting_list():
            file.write(f"{setting}")


def load_settings(path: str, project_name: str) -> Setting:
    if not os.path.exists(path): return
    setting_list = []

    with open(f"{path}/{project_name}_misc.csv", "r") as file:
            text = csv.reader(file, delimiter=",")

            for row in text:
                setting_list.append(row)

    return Setting(setting_list[0], setting_list[1], setting_list[2])


