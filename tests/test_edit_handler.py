from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from wagtail.tests.utils import WagtailTestUtils


class TestEditHandler(StaticLiveServerTestCase, WagtailTestUtils):
    @classmethod
    def setUpClass(cls):
        super(TestEditHandler, cls).setUpClass()
        cls.driver = webdriver.PhantomJS()
        cls.driver.set_window_size(1920, 1080)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        print('tearing down')
        cls.driver.quit()
        super(TestEditHandler, cls).tearDownClass()

    def setUp(self):
        self.create_test_user()
        # Admin login
        self.driver.get('%s%s' % (self.live_server_url, '/admin/login/'))
        username_input = self.driver.find_element_by_id('id_username')
        username_input.send_keys('test@email.com')
        password_input = self.driver.find_element_by_id('id_password')
        password_input.send_keys('password')
        self.driver.save_screenshot('screenshots/logging_in.png')
        self.driver.find_element_by_css_selector('li.submit > button').click()
        self.driver.save_screenshot('screenshots/logged_in.png')

    def test_create_annotation(self):
        self.driver.get('%s%s' % (self.live_server_url, '/admin/'))
        self.driver.save_screenshot('screenshots/creation.png')
