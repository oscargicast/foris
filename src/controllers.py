import importlib

from pathlib import Path
from typing import Union
from src.models import Student, Presence, Report


class GenerateReport:

    def __init__(self, input_file_path) -> None:
        self.input_file_path = input_file_path
        self.output_file_path = self._get_output_file_path()
        Report.clean_instances()

    def generate(self):
        try:
            with open(self.input_file_path, 'r') as input_file:
                for line in input_file:
                    self.run_command(line.strip())
            sorted_reports = self.compute_reports()
            return self.create_output_file(
                report_entries=sorted_reports,
                output_file_path=self.output_file_path,
            )
        except FileNotFoundError:
            raise FileNotFoundError("File not found")

    def run_command(self, entry: str) -> None:
        command, *args = entry.split(' ')
        CommandClass = self._get_the_class(class_name=command)
        instance = CommandClass(*args)
        if not instance:
            return
        if CommandClass == Student:
            report = Report(student=instance)
        if CommandClass == Presence:
            report = Report(student=instance.student)
            report.add_presence(presence=instance)

    def _get_the_class(self, class_name: str) -> Union[Student, Presence]:
        # Import the models.py module.
        module = importlib.import_module('src.models')
        # Dynamically get the class from the module.
        try:
            return getattr(module, class_name)
        except AttributeError:
            raise ValueError(
                f"Invalid command. Check your input file: '{self.input_file_path}'"
            )

    def compute_reports(self):
        report_instances = Report._instances
        report_list = []
        for report in report_instances.values():
            report_obj = report['class']
            report_obj.compute_minutes_and_days()
            report_list.append(report_obj)
        report_list.sort(reverse=True)
        return report_list

    def _get_output_file_path(self) -> str:
        input_path = Path(self.input_file_path)
        output_path = input_path.with_name(f"output_{input_path.name}")
        return str(output_path)

    @staticmethod
    def create_output_file(report_entries: list[Report], output_file_path: str) -> str:
        with open(output_file_path, "w") as output_file:
            for index, report in enumerate(report_entries):
                report_line = report.print_report()
                output_file.write(f"{report_line}")
                if index != len(report_entries) - 1:
                    output_file.write("\n")
                print(report_line)
        return output_file_path