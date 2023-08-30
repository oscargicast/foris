import argparse
import os
import pytest
import sys

from rich import print
from src.controllers import GenerateReport


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def setup_python_path():
    # Add the src directory to the Python path.
    src_dir = os.path.join(PROJECT_ROOT, "src")
    sys.path.insert(0, src_dir)

def test_command(args: list["str"]):
    print(
        "\n[bold green]:microbe::microbe: "
        "Running tests... "
        ":microbe::microbe:[/bold green]\n"
    )
    setup_python_path()
    pytest.main(args)

def generate_report_command(filename: argparse.Namespace):
    file_path = filename.filename
    print(
        "\n[bold red]:beer::beer: "
        "Generating report! "
        ":beer::beer:[/bold red]\n"
        f"[bold green]Input file:[/bold green] {file_path}"
    )
    GenerateReport(file_path).generate()

def main():
    parser = argparse.ArgumentParser(
        description="Generates a student attendance report",
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Subparser for 'test' command.
    subparsers.add_parser("test", help="Run all tests")

    # Subparser for 'generate_report' command.
    generate_report_parser = subparsers.add_parser(
        "generate_report",
        help="Generate a report",
    )
    generate_report_parser.add_argument(
        "filename",
        help="Path to the input file to analize",
    )
    generate_report_parser.set_defaults(func=generate_report_command)

    # Get the args.
    args, extra_args = parser.parse_known_args()

    # In case there is no command.
    if not getattr(args, "command"):
        print(
            "No command provided :pensive_face:. "
            "Use --help to see available commands."
        )
        return
    # In order to handle args with the "-" prefix for the test command.
    if args.command == "test":
        test_command(extra_args)
    # For the other commands, in this case just generate_report.
    if hasattr(args, "func"):
        args.func(args)


if __name__ == "__main__":
    main()
