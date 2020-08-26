import time
import uuid

from chorus_ai_page_objects import EMAIL, PASSWORD, LoginPage, MeetingPage
import pytest
from webdriver import chrome_driver


class BaseTest:

    @pytest.fixture(scope='function', autouse=True)
    def start_and_end_test(self):
        self.driver = chrome_driver()
        self.driver.get('https://chorus.ai/')
        yield
        self.driver.close()
        self.driver.quit()

    @pytest.fixture()
    def login_fixture(self):
        self.driver.get('https://chorus.ai/meeting/3519739?tab=summary&call=07373DE47C6246A1B39F62311C156162')
        LoginPage.login_options.wait_for_visibility()
        LoginPage.login_options[4].click()
        LoginPage.login_email_field.send_keys(EMAIL)
        LoginPage.login_email_field.send_keys(PASSWORD)
        LoginPage.login_button.click()
        MeetingPage.video_screen.wait_for_visibility()


class TestMeetingFunctions(BaseTest):

    def test_player_behaviour(self, login_fixture):
        assert '0:00' in MeetingPage.current_play_time.text, "play time is not currently at 0:00"
        MeetingPage.skip_forward_button.click()
        assert '0:15' in MeetingPage.current_play_time.text, "play time did not move to 0:15"
        MeetingPage.skip_back_button.click()
        assert '0:00' in MeetingPage.current_play_time.text, "play time is not back to 0:00"
        MeetingPage.play_pause_button.click()
        time.sleep(2)
        assert '0:00' not in MeetingPage.current_play_time.text, "time did not change after hitting play"
        MeetingPage.play_pause_button.click()

    def test_comments_section(self, login_fixture):
        random_text = uuid.uuid4()
        play_time = MeetingPage.current_play_time.text
        MeetingPage.comments_button.click()
        before_item_count = len(MeetingPage.comment_item)
        MeetingPage.add_comment_field.send_keys(random_text)
        MeetingPage.add_comment_button.click()
        counter = 0
        while len(MeetingPage.comment_item) == before_item_count:
            time.sleep(1)
            counter += 1
            if counter <= 5:
                assert 0, "comment did not add in 5 seconds!"
        assert len(MeetingPage.comment_item) - 1 == before_item_count, "comments did not increase by 1!"
        comment_time_stamp = MeetingPage.comment_item[-1].find_element_by_class_name('timestamp').text
        assert comment_time_stamp in play_time, \
            f"comment was added with wrong time code! expected: {play_time}, got: {comment_time_stamp}"

    def test_transcription(self, login_fixture):
        MeetingPage.view_transcript.click()
        assert len(MeetingPage.transcript_elements) > 3, "transcript is no more than 3 items!"
