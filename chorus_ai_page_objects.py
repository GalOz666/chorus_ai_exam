import selenium
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from webdriver import chrome_driver

TIME_OUT = 5
EMAIL = 'test900@chorus-auto.com'
PASSWORD = 'KCGo1Dvp4P!'


class BaseElement:

    _driver = chrome_driver()

    def __init__(self, locator, by=By.CSS_SELECTOR):
        self.locator = locator
        self.by = by

    def __iter__(self):
        return (x for x in self._driver.find_elements(self.by, self.locator))

    def __getitem__(self, item):
        if isinstance(item, int):
            return list(self.__iter__())[item]
        else:
            raise IndexError

    def __len__(self):
        return len(list(self.__iter__()))

    def wait_for_visibility(self, time_out=TIME_OUT):
        return WebDriverWait(self._driver, time_out).until(
            expected_conditions.visibility_of_element_located((self.by, self.locator)))

    def click(self, time_out=TIME_OUT):
        element = WebDriverWait(self._driver, time_out).until(
            expected_conditions.element_to_be_clickable((self.by, self.locator)))
        return element.click()

    def send_keys(self, keys):
        element = self.wait_for_visibility()
        try:
            element.click()
            element.clear()
        except RuntimeError:
            pass
        element.send_keys(keys)


class LoginPage:

    login_options = BaseElement(locator='.mat-button-wrapper')
    login_email_field = BaseElement(locator='input[type="email"]')
    login_password_field = BaseElement(locator='input[type="password"]')
    login_button = BaseElement(locator='.login-button')


class MeetingPage:

    video_screen = BaseElement(locator='.video card spring')
    play_pause_button = BaseElement(locator='play-pause[class^="ng-tns"]')
    player_timer = BaseElement(locator='.timestamp span')
    current_play_time = player_timer[0]
    total_play_time = player_timer[1]
    skip_back_button = BaseElement(locator='i[class="an-back-15"]')
    skip_forward_button = BaseElement(locator='i[class="an-back-15"]')
    view_transcript = BaseElement(locator='.view-full-transcript')
    transcript_elements = BaseElement(locator='.snippet-speaker')
    comments_button = BaseElement(locator='chorus-icon[iconname="an-comment"]')
    comment_item = BaseElement(locator='.comment-block')
    add_comment_field = BaseElement(locator='#mat-input-4')
    add_comment_button = BaseElement(locator='div.action-buttons > button')

