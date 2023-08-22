import os
import pytest
import sys

from src.controllers import GenerateReport


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def setup_python_path():
    # Add the src directory to the Python path.
    src_dir = os.path.join(PROJECT_ROOT, "src")
    sys.path.insert(0, src_dir)

def get_input_file_path():
    if len(sys.argv) == 3:
        arg = sys.argv[2]
        return arg
    else:
        raise("A input filename must be specified")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./manage.py <command>")
        sys.exit(1)

    command = sys.argv[1]
    if command == "test":
        setup_python_path()
        pytest.main(sys.argv[2:])
    elif command == "generate_report":
        file_path = get_input_file_path()
        GenerateReport(file_path).generate()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
