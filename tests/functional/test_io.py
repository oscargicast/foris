from hamcrest import assert_that, equal_to

from src.controllers import GenerateReport


def test_reports(io_data_fixture):
    input_file_path, expected_output_file_path = io_data_fixture
    print(f"\nTesting : {input_file_path}")
    print(f"Expected: {expected_output_file_path}")
    output_file_path = GenerateReport(input_file_path).generate()
    with open(output_file_path, "rb") as f1, open(expected_output_file_path, "rb") as f2:
        content1 = f1.read()
        content2 = f2.read()
        assert_that(content1, equal_to(content2))