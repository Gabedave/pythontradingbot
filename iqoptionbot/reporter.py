"""Module for Trading bot reporter."""
from datetime import datetime
import json

class Report:
    def __init__(self) -> None:
        pass

    def report(self, tradeid_list, file_path):
        self.data = []
        for id in tradeid_list:
            self.data.append({"datetime":str(datetime.utcnow()),"id":id})

            with open(file_path, "a") as report_file:
                json.dump(self.data, report_file, indent=4)
