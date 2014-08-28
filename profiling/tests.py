# Django
from django.contrib.staticfiles.testing import StaticLiveServerCase
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.test import TestCase, Client, RequestFactory

# Ours
from coffee.factories import CoffeeFactory
from profiling.factories import PointCommentFactory
from profiling.models import PointComment
import ajax
import forms

# Third Party
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import ui

# Python
import time


class TestRoastProfileDetail(StaticLiveServerCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(TestRoastProfileDetail, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(TestRoastProfileDetail, cls).tearDownClass()

    def setUp(self):
        self.coffee = CoffeeFactory.create()
        self.coffee._generate_profile()
        self.roastprofile = self.coffee.roastprofile_set.all()[0]

    def tearDown(self):
        self.coffee.delete()

    def test_comment_form_create_and_post(self):
        """
        Test that a user can create a comment from the roastprofile detail page.
        """

        self.selenium.get(
            '%s%s' % (
                self.live_server_url, 
                reverse('roastprofile-detail', args=(self.roastprofile.id,))
            )
        )
 
        # Wait for page to fully load // TODO: Find a better way, I should never have to use time.sleep in
        # a test.  If it takes longer than a second, it could intermittently fail.
        time.sleep(1)

        # Click on the (time=21) point on the chart, which should create a form
        self.selenium.find_element_by_class_name("nv-path-21").click()
        time.sleep(1)  # Wait for the form to be rendered

        # Find the form, if this fails, the form wasn't created.
        comment_form = self.selenium.find_element_by_id('id_comment')
        comment_form.send_keys('My Comment')

        # Select the submit button, submit the form.
        self.selenium.find_element_by_id('submit-pointcomment').click()

        time.sleep(1) # Wait for the form to submit and be rendered
        # Ensure that the submitted comment exists with correct text, and that a new blank form was rendered.
        self.selenium.find_element_by_class_name('comment')
        self.selenium.find_element_by_id('id_comment')

        
        comment = PointComment.objects.filter(comment='My Comment')
        self.assertEqual(comment.exists(), True)

    def test_comment_form_delete(self):
        """
        Test that a user can delete a comment from the roast profile detail page.
        """

        self.selenium.get(
            '%s%s' % (
                self.live_server_url, 
                reverse('roastprofile-detail', args=(self.roastprofile.id,))
            )
        )

        # Grab the first point ( by time ) on a roast profile
        # and create a comment for it
        firstpoint = self.roastprofile.temppoint_set.all().order_by('time')[0]
        newcomment = PointCommentFactory.create(point=firstpoint, comment="Le Commentzorz")
        time.sleep(1)

        # Click on the first point, assert that the comment we just created renders
        self.selenium.find_element_by_class_name("nv-path-0").click()
        self.selenium.find_elements_by_class_name("id_comment")

        time.sleep(1)
        # Assert that we can delete the comment from the page
        self.selenium.find_element_by_css_selector(
            ".comment .comment-delete"
        ).click()
        time.sleep(1)

        comment_query = PointComment.objects.filter(id=newcomment.id)
        self.assertEqual(comment_query.exists(), False)       


class TestAjaxViews(TestCase):

    def setUp(self):
        self.coffee = CoffeeFactory.create()
        self.coffee._generate_profile()
        self.roastprofile = self.coffee.roastprofile_set.all()[0]
        self.request_factory = RequestFactory()

    def tearDown(self):
        self.coffee.delete()

    def test_temppoint_comment_create_form(self):
        some_temppoint = self.roastprofile.temppoint_set.all()[0]
        request = self.request_factory.get(
            reverse('ajax-temppoint-comment-create-form'), 
            {'TempPointID': some_temppoint.id }
        )

        response = ajax.temppoint_comment_create_form(request)
        data = render_to_string(
            '_includes/forms/point_comment_form.jade',
            {
                'point':some_temppoint,
                'form':forms.PointCommentForm(data={'point':some_temppoint.id}),
                'comments': some_temppoint.pointcomment_set.all().order_by('created')
            }
        )
        expected_response = JsonResponse({'data':data})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected_response.content)

    def test_temppoint_comment_create(self):
        some_temppoint = self.roastprofile.temppoint_set.all()[0]
        comment = 'I made a comment dood'
        request = self.request_factory.post(
            reverse('ajax-temppoint-comment-create'),
            {
                'TempPointID': some_temppoint.id,
                'comment': comment,
            }
        )

        response = ajax.temppoint_comment_create(request)

        self.assertEqual(response.status_code, 200)
        comment_queryset = PointComment.objects.filter(point__id=some_temppoint.id, comment=comment)
        self.assertEqual(comment_queryset.exists(), True)
        self.assertEqual(comment_queryset.count(), 1)

    def test_comment_delete(self):
        some_temppoint = self.roastprofile.temppoint_set.all()[0]
        pointcomment = PointCommentFactory.create(point=some_temppoint, comment="Hay")

        request = self.request_factory.post(
            reverse('ajax-comment-delete'),
            {
                'TempPointID':some_temppoint.id,
                'commentID':pointcomment.id    
            }
        )

        self.assertEqual(PointComment.objects.filter(id=pointcomment.id).exists(), True)

        response = ajax.comment_delete(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PointComment.objects.filter(id=pointcomment.id).exists(), False)

    def test_roastprofile_create(self):
        request = self.request_factory.post(
            reverse('ajax-roastprofile-create'),
            {'coffeeID': self.coffee.id}
        )

        self.assertEqual(self.coffee.roastprofile_set.all().count(), 1)

        response = ajax.roastprofile_create(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.coffee.roastprofile_set.all().count(), 2)

    def test_roastprofile_delete(self):
        request = self.request_factory.post(
            reverse('ajax-roastprofile-delete'),
            {'RoastProfileID': self.roastprofile.id}
        )

        self.assertEqual(self.coffee.roastprofile_set.all().count(), 1)

        response = ajax.roastprofile_delete(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.coffee.roastprofile_set.all().exists(), False)

    def test_roastprofile_graph_data(self):
        request = self.request_factory.get(
            reverse('ajax-roastprofile-graph-data'),
            {'roastProfileID': self.roastprofile.id}
        )

        response = ajax.roastprofile_graph_data(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            JsonResponse({'graphData':self.roastprofile.get_temp_graph_data()}).content
        )

    def test_roastprofile_graph_data_slice(self):
        request = self.request_factory.get(
            reverse('ajax-roastprofile-graph-data-slice'),
            {
                'roastProfileID': self.roastprofile.id,
                'sliceStart': '5'
            }
        )

        response = ajax.roastprofile_graph_data_slice(request)

        self.assertEqual(response.status_code, 200)