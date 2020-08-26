from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from webdriver import chrome_driver

TIME_OUT = 5


class BaseElement:

    _driver = chrome_driver()

    def __init__(self, locator, selector=By.CSS_SELECTOR):
        self.locator = locator
        self.selector = selector

    def __iter__(self):
        return self._driver.find_elements(self.selector, self.locator)

    def __len__(self):
        return len(self.__iter__())

    def click(self):
        element = WebDriverWait(self._driver, TIME_OUT).until(
            expected_conditions.element_to_be_clickable((self.selector, self.locator)))
        element.click()
