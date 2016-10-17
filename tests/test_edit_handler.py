import json

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from wagtail.tests.utils import WagtailTestUtils
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.tests.utils import get_test_image_file

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.app.models import TestPage

screenshots = True


class TestEditHandler(StaticLiveServerTestCase, WagtailTestUtils):
    @classmethod
    def setUpClass(cls):
        super(TestEditHandler, cls).setUpClass()
        caps = DesiredCapabilities.PHANTOMJS
        # caps['loggingPrefs'] = { 'browser':'ALL' }
        cls.driver = webdriver.PhantomJS(desired_capabilities=caps)

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

    def setUp(self):
        # Add an image to use
        self.test_image = Image.objects.create(
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

    def save_page(self, title):
        self.driver.find_element_by_id('id_title').send_keys(title)
        actions = self.driver.find_element_by_css_selector('li.actions ')
        actions.find_element_by_css_selector('div.dropdown-toggle').click()
        actions.find_element_by_xpath('//button[@value="action-publish"]').click()
        message = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.messages > ul > li'))
        )
        self.assertTrue('success' in message.get_attribute('class'))

    def test_create_annotation(self):
        self.driver.get('%s%s' % (self.live_server_url, '/admin/pages/add/app/testpage/1/'))
        annotation_container = self.driver.find_element_by_id('id_image-annotation-container')
        annotation_container.find_element_by_xpath('//div[@id="id_image-chooser"]/div/button').click()
        element = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="search"]//a'))
        )
        self.ss('chooser_open')
        element.click()
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.XPATH, '//*[@id="search"]//a'))
        )
        self.ss('image_chosen')
        for entry in self.driver.get_log('browser'):
            print(entry)
        preview_image = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-image-container] > img'))
        )
        self.ss('preview_rendered')
        self.assertEqual('%s/media/images/test.original.png' % self.live_server_url, preview_image.get_attribute('src'))

        annotation_action = ActionChains(self.driver)
        annotation_action.move_to_element_with_offset(preview_image, 50, 50)
        annotation_action.click()
        annotation_action.perform()
        self.ss('annotation_added')
        annotation_marker = annotation_container.find_element_by_css_selector('[data-image-container] > span')
        self.assertEqual(annotation_marker.text, '1')
        annotation_form = annotation_container.find_element_by_css_selector('[data-annotation-forms] > div')
        self.assertEqual(annotation_form.find_element_by_tag_name('h3').text, '1')
        self.assertEqual(annotation_form.find_element_by_id('id_annotation_number').get_attribute('value'), '1')
        annotation_form.find_element_by_id('id_text').send_keys('Unwanted textual advances')
        annotation_form.click()  # Lose focus

        annotation_data_field = self.driver.find_element_by_id('id_annotations')
        annotation_json = json.loads(annotation_data_field.get_attribute('value'))
        self.assertEqual(annotation_json['1']['fields']['text'], 'Unwanted textual advances')
        self.ss('annotation_text')
        title = 'one annotation'
        self.save_page(title)
        self.ss('page_save')

        page = TestPage.objects.get(title=title)
        self.assertEqual(page.image, self.test_image)
        self.assertEqual(page.annotations, annotation_json)
