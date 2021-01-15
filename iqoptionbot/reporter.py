"""Module for Trading bot reporter."""
import json

class Report:
    def __init__(self) -> None:
        pass

    def report(self, tradeid_list, file_path):
        self.__report_data = tradeid_list

        for id in self.__report_data:
            with open(file_path, "a") as report_file:
                json.dump(id, report_file, indent=4)
