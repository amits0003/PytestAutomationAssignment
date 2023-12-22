import os
import subprocess
import pytest


def run_tests_and_generate_individual_reports():
    # Get the current directory of the script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Go to the parent directory
    parent_directory = os.path.dirname(current_directory)

    # Go to the test directory
    test_directory = os.path.join(parent_directory, 'test')
    os.chdir(test_directory)

    # Get a list of all files in the test directory
    test_files = [file for file in os.listdir() if file.endswith('.py')]

    # Run all test files using pytest and collect results
    individual_reports = []
    for test_file in test_files:
        if not test_file.startswith("__"):
            output_html_report = f"output_{test_file}.html"
            # command = f"pytest {test_file} --html={output_html_report}"
            command = f"\"{os.path.join(parent_directory, '.venv', 'Scripts', 'pytest')}\" {test_file} --html={output_html_report}"
            subprocess.run(command, shell=True)
            individual_reports.append(output_html_report)

    # combined_report_path = f"combined_report.html"
    # combine_command = f"{os.path.join(parent_directory, '.venv', 'Scripts', 'pytest')} {' '.join(individual_reports)} --html={combined_report_path}"
    # subprocess.run(combine_command, shell=True)


if __name__ == "__main__":
    run_tests_and_generate_individual_reports()
