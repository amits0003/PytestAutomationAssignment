import inspect
import os
import unittest
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from utilities.log_event_handler import log_event
import allure


@pytest.mark.flaky(reruns=2)
class BaseTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        # This setup method will run before each test method
        # self.log_event = logger  # Create a logger instance
        self.driver = None  # Initialize the driver
        self.allure = allure

    def log_test_result(self):
        function_name = self.id().split('.')[-1]
        log_event.info(f"Test case: {function_name} passed")

    def wrapper(self):
        function_name = self.id().split('.')[-1]
        test_case_lines = inspect.getsourcelines(self.__class__)[0]

        for line_number, line in enumerate(test_case_lines, start=1):
            line = line.strip()
            if line.startswith("def ") and line.endswith(":"):
                continue  # Skip method definition lines

            try:
                exec(line)  # Execute the line
                log_event.info(f"Test case '{function_name}': Line {line_number} passed")
            except Exception as e:
                log_event.error(f"Test case '{function_name}': Line {line_number} failed - {str(e)}")

        log_event.info(f"Test case '{function_name}' passed")

    def tearDown(self):
        # This teardown method will run after each test method
        if self.driver:
            self.driver.quit()  # Close the browser

    @staticmethod
    def launchBrowser(browser_name):
        """
        supported browsers : Chrome, Firefox, Internet Explorer (Ie)
        """
        browser_name = browser_name.lower()

        if browser_name == 'chrome':
            driver_manager = ChromeDriverManager()
        elif browser_name == 'firefox':
            driver_manager = GeckoDriverManager()
        elif browser_name == 'ie':
            driver_manager = IEDriverManager()
        else:
            raise ValueError("Invalid browser choice")

        driver_path = driver_manager.install()

        if not os.path.exists(driver_path):
            raise Exception("Driver installation failed. Please check the browser choice and try again.")

        if browser_name == 'chrome':
            # options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            return webdriver.Chrome()
        elif browser_name == 'firefox':
            return webdriver.Firefox()
        elif browser_name == 'ie':
            return webdriver.Ie()


class CustomTestRunner(BaseTest):
    def run(self, test):
        result = super().run(test)
        if hasattr(test, 'wrapper'):
            test.wrapper()
        return result
