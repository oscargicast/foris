import os
import re
import pytest

from typing import Dict


def pytest_generate_tests(metafunc):
    """
    Map for each input file the expected results.

    io_files will have the structure:
        {
            input1.txt: expected_output1.txt,
            input2.txt: expected_output2.txt,
            ...
        }
    """
    if "io_data_fixture" in metafunc.fixturenames:
        io_files: Dict[str, str] = {}
        for filename in os.listdir("tests/test_data"):
            if not filename.startswith("input"):
                continue
            match = re.search(r'\d+', filename)
            if not match:
                continue
            correlative_number = int(match.group())
            io_files[f"input{correlative_number}.txt"] = f"expected_output{correlative_number}.txt"
        metafunc.parametrize("io_data_fixture", list(io_files.items()), indirect=True)

@pytest.fixture
def io_data_fixture(request):
    input_filename, output_filename = request.param
    # Set input.
    input_file_path = os.path.join("tests", "test_data", input_filename)
    # Set output.
    output_file_path = os.path.join("tests", "test_data", output_filename)
    return input_file_path, output_file_path

def delete_generated_files(request):
    for filename in os.listdir("tests/test_data"):
        if not filename.startswith("output_"):
            continue
        path_to_delete = f"tests/test_data/{filename}"
        if os.path.exists(path_to_delete):
            os.remove(path_to_delete)

# Register the function with the pytest_runtest_teardown hook.
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    delete_generated_files(item)