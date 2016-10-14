from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from wagtail.tests.utils import WagtailTestUtils
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.tests.utils import get_test_image_file


class TestEditHandler(StaticLiveServerTestCase, WagtailTestUtils):
    @classmethod
    def setUpClass(cls):
        super(TestEditHandler, cls).setUpClass()
        cls.driver = webdriver.Firefox()
        cls.driver.set_window_size(1920, 1080)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(TestEditHandler, cls).tearDownClass()

    # helpful for debugging (folder needs to exist)
    def ss(self, name):
        self.driver.save_screenshot('tests/screenshots/%s.png' % name)

    def setUp(self):
        # Add an image to use
        Image.objects.create(
            title='test-image',
            file=get_test_image_file(colour='red'),
        )
        # Login the webdriver
        self.create_test_user()
        self.driver.get('%s%s' % (self.live_server_url, '/admin/login/'))
        username_input = self.driver.find_element_by_id('id_username')
        username_input.send_keys('test@email.com')
        password_input = self.driver.find_element_by_id('id_password')
        password_input.send_keys('password')
        self.driver.find_element_by_css_selector('li.submit > button').click()
        self.driver.save_screenshot('screenshots/logged_in.png')

    def test_create_annotation(self):
        self.driver.get('%s%s' % (self.live_server_url, '/admin/pages/add/app/testpage/1/'))
        annotation_container = self.driver.find_element_by_id('id_image-annotation-container')
        annotation_container.find_element_by_xpath('//div[@id="id_image-chooser"]/div/button').click()
        element = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="search"]//a'))
        )
        self.ss('chooser')
        element.click()
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.XPATH, '//*[@id="search"]//a'))
        )
        self.ss('chosen')
        # MutationObserver js not working?
        # print(annotation_container.get_attribute("outerHTML"))
        preview_image = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-image-container] > img'))
        )
        self.ss('preview')
        print(preview_image.get_attribute('src'))
