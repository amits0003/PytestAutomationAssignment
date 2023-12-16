from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebControl:

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def navigate_to_url(driver, url):
        return driver.get(url)

    @staticmethod
    def get_web_title(driver):
        return driver.title

    @staticmethod
    def click_on_ID(driver, req_ID):
        return driver.find_element(By.ID, req_ID).click()

    @staticmethod
    def click_on_XPATH(driver, req_XPATH):
        return driver.find_element(By.XPATH, req_XPATH).click()

    @staticmethod
    def click_on_LINK_TEXT(driver, req_LINK_TEXT):
        return driver.find_element(By.LINK_TEXT, req_LINK_TEXT).click()

    @staticmethod
    def click_on_TAG_NAME(driver, req_TAG_NAME):
        return driver.find_element(By.TAG_NAME, req_TAG_NAME).click()

    @staticmethod
    def click_on_CLASS_NAME(driver, req_CLASS_NAME):
        return driver.find_element(By.CLASS_NAME, req_CLASS_NAME).click()

    @staticmethod
    def click_on_CSS_SELECTOR(driver, req_CSS_SELECTOR):
        return driver.find_element(By.CSS_SELECTOR, req_CSS_SELECTOR).click()

    @staticmethod
    def find_element_by_ID(driver, req_ID):
        return driver.find_element(By.ID, req_ID)

    @staticmethod
    def find_element_by_XPATH(driver, req_XPATH):
        return driver.find_element(By.XPATH, req_XPATH)

    @staticmethod
    def find_element_by_LINK_TEXT(driver, req_LINK_TEXT):
        return driver.find_element(By.LINK_TEXT, req_LINK_TEXT)

    @staticmethod
    def find_element_by_TAG_NAME(driver, req_TAG_NAME):
        return driver.find_element(By.TAG_NAME, req_TAG_NAME)

    @staticmethod
    def find_element_by_CLASS_NAME(driver, req_CLASS_NAME):
        return driver.find_element(By.CLASS_NAME, req_CLASS_NAME)

    @staticmethod
    def find_element_by_CSS_SELECTOR(driver, req_CSS_SELECTOR):
        return driver.find_element(By.CSS_SELECTOR, req_CSS_SELECTOR)

    @staticmethod
    def find_elements_by_ID(driver, req_ID):
        return driver.find_elements(By.ID, req_ID)

    @staticmethod
    def find_elements_by_XPATH(driver, req_XPATH):
        return driver.find_elements(By.XPATH, req_XPATH)

    @staticmethod
    def find_elements_by_LINK_TEXT(driver, req_LINK_TEXT):
        return driver.find_elements(By.LINK_TEXT, req_LINK_TEXT)

    @staticmethod
    def find_elements_by_TAG_NAME(driver, req_TAG_NAME):
        return driver.find_elements(By.TAG_NAME, req_TAG_NAME)

    @staticmethod
    def find_elements_by_CLASS_NAME(driver, req_CLASS_NAME):
        return driver.find_elements(By.CLASS_NAME, req_CLASS_NAME)

    @staticmethod
    def find_elements_by_CSS_SELECTOR(driver, req_CSS_SELECTOR):
        return driver.find_elements(By.CSS_SELECTOR, req_CSS_SELECTOR)

    @staticmethod
    def clearTextField(driver, by_selector, by_element):
        driver.find_element(by_selector, by_element).clear()

    @staticmethod
    def enter_value_on(driver, by_selector, by_element, value):
        driver.find_element(by_selector, by_element).clear()
        return driver.find_element(by_selector, by_element).send_keys(value)

    @staticmethod
    def waitForElementVisibility(driver, by_selector, by_element):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((by_selector, by_element)))

