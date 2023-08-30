from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table
from src.models import Student, Presence, ShortPresenceError
from enum import Enum


class Command(Enum):
    STUDENT = 'Student'
    PRESENCE = 'Presence'


class CommandError(Exception):
    ...


class GenerateReport:

    def __init__(self, input_file_path: str) -> None:
        self.input_file_path = input_file_path
        self.output_file_path = self._get_output_file_path()
        self.students: dict[str, Student] = {}

    def generate(self):
        try:
            with open(self.input_file_path, 'r') as input_file:
                for line in input_file:
                    self.run_command(line.strip())
            sorted_students: list[Student] = self.get_sorted_students()
            self.print_report_table(sorted_students)
            return self.create_output_file(
                output_file_path=self.output_file_path,
                students=sorted_students,
            )
        except FileNotFoundError:
            raise FileNotFoundError("File not found")

    def get_sorted_students(self) -> list[Student]:
        return sorted(self.students.values(), reverse=True)

    def get_student(self, name: str) -> Student:
        if name not in self.students:
            self.students[name] = Student(name)
        return self.students[name]

    def run_command(self, entry: str) -> None:
        command, name, *args = entry.split(' ')
        if command == Command.STUDENT.value:
            student = self.get_student(name)
        elif command == Command.PRESENCE.value:
            student = self.get_student(name)
            try:
                presence = Presence(*args)
            except ShortPresenceError:
                return
            student.register_presence(presence)
        else:
            raise CommandError("Unknown command")

    def _get_output_file_path(self) -> str:
        input_path = Path(self.input_file_path)
        output_path = input_path.with_name(f"output_{input_path.name}")
        return str(output_path)

    @classmethod
    def print_report_table(cls, students: list[Student]):
        table = Table(title="Student Presence Report")
        table.add_column("Student", style="cyan", no_wrap=True)
        table.add_column("Minutes", style="magenta")
        table.add_column("Days", justify="right", style="green")
        for student in students:
            table.add_row(
                student.name,
                str(student.minutes),
                str(student.days),
            )
        console = Console()
        console.print(table)

    @classmethod
    def create_output_file(cls, output_file_path: str,
                           students: list[Student]) -> str:
        print(
            f"[bold green]Output file:[/bold green] {output_file_path}\n"
        )
        with open(output_file_path, "w") as output_file:
            for index, student in enumerate(students):
                report_line = student.print_report()
                output_file.write(f"{report_line}")
                if index != len(students) - 1:
                    output_file.write("\n")
                print(report_line)
        return output_file_path