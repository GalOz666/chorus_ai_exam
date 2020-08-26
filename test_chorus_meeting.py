import selenium
import pytest
from webdriver import chrome_driver


class BaseTest:

    @pytest.fixture(scope='function')
    def start_and_end_test(self):
        self.driver = chrome_driver()
        yield
        self.driver.close()
        self.driver.quit()

    def login_fixture(self):


