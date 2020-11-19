import json

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from wagtail.images.models import Image
from wagtail.images.tests.utils import get_test_image_file
from wagtail.tests.utils import WagtailTestUtils

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tests.app.models import TestPage

# Screenshot flag
screenshots = False

class TestEditHandler(StaticLiveServerTestCase, WagtailTestUtils):
    @classmethod
    def setUpClass(cls):
        super(TestEditHandler, cls).setUpClass()
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cap = DesiredCapabilities.CHROME.copy()
        cap['loggingPrefs'] = { 'browser':'ALL' }
        cap['goog:loggingPrefs'] = { 'browser':'ALL' }
        cls.driver = webdriver.Chrome(desired_capabilities=cap, chrome_options=options)

        cls.driver.set_window_size(1920, 1080)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(TestEditHandler, cls).tearDownClass()

    # helpful for debugging (folder needs to exist)
    def ss(self, name):
        if screenshots:
            self.driver.save_screenshot('tests/screenshots/%s.png' % name)

    # Debugger for js errors
    def print_js_console(self):
        for entry in self.driver.get_log('browser'):
            print(entry)

    def setUp(self):
        # Add an image to use
        self.test_image = Image.objects.create(
            title='test-image',
            file=get_test_image_file(colour='red'),
        )
        # Login the webdriver
        self.create_test_user()
        self.driver.get('%s%s' % (self.live_server_url, '/admin/login/'))
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.send_keys('test@email.com')
        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.send_keys('password')
        self.driver.find_element(By.CSS_SELECTOR, 'li.submit > button').click()
        self.driver.save_screenshot('screenshots/logged_in.png')

    def save_page(self, title):
        self.driver.find_element(By.ID, 'id_title').send_keys(title)
        self.driver.find_element(By.XPATH, '//a[@href="#tab-promote"]').click()
        self.driver.find_element(By.ID, 'id_slug').send_keys('cool-slug')
        actions = self.driver.find_element(By.CSS_SELECTOR, 'li.actions ')
        actions.find_element(By.CSS_SELECTOR, 'div.dropdown-toggle').click()
        actions.find_element(By.XPATH,
            '//button[@value="action-publish"]').click()
        message = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '.messages > ul > li'))
        )
        self.ss('page_save')
        self.assertTrue('success' in message.get_attribute('class'))

    def test_create_annotation(self):
        self.driver.get('%s%s' % (self.live_server_url,
                                  '/admin/pages/add/app/testpage/1/'))
        annotation_container = self.driver.find_element(
            By.ID, 'id_image-annotation-container')
        annotation_container.find_element(
            By.XPATH,
            '//div[@id="id_image-chooser"]/div/button').click()
        element = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="search"]//a'))
        )
        self.ss('chooser_open')
        element.click()
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located(
                (By.XPATH, '//*[@id="search"]//a'))
        )
        self.ss('image_chosen')
        preview_image = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-image-container] > img'))
        )
        self.ss('preview_rendered')
        self.assertEqual('%s/media/images/test.original.png' %
                         self.live_server_url, preview_image.get_attribute('src'))

        annotation_action = ActionChains(self.driver)
        annotation_action.move_to_element_with_offset(preview_image, 50, 50)
        annotation_action.click()
        annotation_action.perform()
        self.ss('annotation_added')
        annotation_marker = annotation_container.find_element(
            By.CSS_SELECTOR, '[data-image-container] > span')
        self.assertEqual(annotation_marker.text, '1')
        annotation_form = annotation_container.find_element(
            By.CSS_SELECTOR, '[data-annotation-forms] > div')
        self.assertEqual(
            annotation_form.find_element(By.TAG_NAME, 'h3').text, '1')
        self.assertEqual(annotation_form.find_element(By.XPATH,
            '//input[@name="annotation-annotation_number"]').get_attribute('value'), '1')
        annotation_input = annotation_form.find_element(By.XPATH, '//input[@name="annotation-text"]')
        annotation_input.send_keys('Unwanted textual advances')
        annotation_input.send_keys(Keys.TAB)
        annotation_form.click()  # Lose focus

        WebDriverWait(self.driver, 30).until(
            EC.text_to_be_present_in_element_value(
                (By.ID, 'id_annotations'), 'Unwanted textual advances')
        )
        annotation_data_field = self.driver.find_element(
            By.ID, 'id_annotations')
        annotation_json = json.loads(
            annotation_data_field.get_attribute('value'))

        self.assertEqual(
            annotation_json['1']['fields']['text'], 'Unwanted textual advances')
        self.ss('annotation_text')
        title = 'one annotation'
        self.save_page(title)

        page = TestPage.objects.get(title=title)
        self.assertEqual(page.image, self.test_image)
        self.assertEqual(page.annotations, annotation_json)
