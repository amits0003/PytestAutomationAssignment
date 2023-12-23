import os
import subprocess


def run_tests_and_generate_allure_report():
    # Get the current directory of the script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Go to the parent directory
    parent_directory = os.path.dirname(current_directory)

    # Go to the test directory
    test_directory = os.path.join(parent_directory, 'test')
    os.chdir(test_directory)

    # Get a list of all files in the test directory
    test_files = [file for file in os.listdir() if file.endswith('.py')]

    # Run all test files using pytest and generate individual allure reports
    for test_file in test_files:
        if not test_file.startswith("__"):
            allure_results_directory = f"allure-results-{test_file}"
            command = f"\"{os.path.join(parent_directory, '.venv', 'Scripts', 'pytest')}\" {test_file} --alluredir={allure_results_directory}"
            subprocess.run(command, shell=True)

    # Combine individual Allure reports into a single report
    combined_allure_report_directory = "allure-results-combined"
    command = "allure generate --clean " + ' '.join([f'allure-results-{test_file}' for test_file in test_files if
                                                     not test_file.startswith(
                                                         "__")]) + f" -o {combined_allure_report_directory}"
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    run_tests_and_generate_allure_report()
