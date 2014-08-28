# Django
from django.contrib.staticfiles.testing import StaticLiveServerCase
from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

# Ours
from coffee.factories import CoffeeFactory
from profiling.factories import PointCommentFactory
from profiling.models import PointComment

# Third Party
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import ui

# Python
import time


class TestRoastProfileDetail(StaticLiveServerCase):
    #fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.coffee = CoffeeFactory.create()
        cls.coffee._generate_profile()
        cls.roastprofile = cls.coffee.roastprofile_set.all()[0]
        super(TestRoastProfileDetail, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        cls.coffee.delete()
        super(TestRoastProfileDetail, cls).tearDownClass()

    def test_comment_form_create_and_post(self):
        self.selenium.get(
            '%s%s' % (
                self.live_server_url, 
                reverse('roastprofile-detail', args=(self.roastprofile.id,))
            )
        )
 
        # Wait for page to fully load // TODO: Find a better way...
        time.sleep(1)

        # Click on the (time=21) point on the chart, which should create a form
        self.selenium.find_element_by_class_name("nv-path-21").click()
        time.sleep(1)  # Wait for the form to be rendered

        # Find the form, if this fails, the form wasn't created.
        comment_form = self.selenium.find_element_by_id('id_comment')
        comment_form.send_keys('My Comment')

        # Select the submit button, submit the form.
        self.selenium.find_element_by_id('submit-pointcomment').click()

        # Ensure that the submitted comment exists with correct text, and that a new blank form was rendered.
        self.selenium.find_elements_by_class_name('comment')
        self.selenium.find_element_by_id('id_comment')

        comment = PointComment.objects.filter(comment='My Comment')
        assert comment.exists()

    # def test_comment_form_delete(self):
    #     self.selenium.get(
    #         '%s%s' % (
    #             self.live_server_url, 
    #             reverse('roastprofile-detail', args=(self.roastprofile.id,))
    #         )
    #     )

    #     firstpoint = self.roastprofile.temppoint_set.all().order_by('time')[0].id
        
    #     newcomment = PointCommentFactory.create(point=firstpoint)
        
        


