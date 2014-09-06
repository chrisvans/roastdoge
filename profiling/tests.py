# Django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.test import TestCase, Client, RequestFactory

# Ours
from coffee.factories import CoffeeFactory
import factories
import models
import ajax
import forms
import views

# Third Party
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import ui
from rest_framework.test import APIRequestFactory

# Python
import time


class TestRoastProfileDetailFunctional(StaticLiveServerTestCase):
    """
    Test that the front-end user interface for the roast profile detail view / charts 
    works as expected.
    """

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(TestRoastProfileDetailFunctional, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(TestRoastProfileDetailFunctional, cls).tearDownClass()

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

        
        comment = models.PointComment.objects.filter(comment='My Comment')
        self.assertEqual(comment.exists(), True)

        # TODO: Test that the comment svg is properly created and placed on the chart.

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
        newcomment = factories.PointCommentFactory.create(point=firstpoint, comment="Le Commentzorz")
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

        comment_query = models.PointComment.objects.filter(id=newcomment.id)
        self.assertEqual(comment_query.exists(), False)

    def test_select_roastprofile_dropdown(self):
        """
        Test that a user can click on the dropdown list of roastprofiles, and that data is 
        properly rendered in the chart.
        """

        self.coffee._generate_profile()

        self.selenium.get(
            '%s%s' % (
                self.live_server_url, 
                reverse('roastprofile-detail', args=(self.roastprofile.id,))
            )
        )

        generated_rp = models.RoastProfile.objects.exclude(id=self.roastprofile.id).get()

        self.selenium.find_element_by_css_selector(
            "select#id_roastprofile_select > option[value='%s']" % generated_rp.id
        ).click()

        time.sleep(1)

        waiting = True
        timeout = 10
        count = 0
        while waiting:
            try:
                for index, point in enumerate(generated_rp.temppoint_set.all()):
                    self.selenium.find_element_by_css_selector(
                        "g.nv-group.nv-series-1 .nv-point-%s" % index
                    ).click()
                waiting = False
            except NoSuchElementException as e:
                if count > timeout:
                    raise e
                time.sleep(1)
            count += 1
        waiting = None


    def test_record_newprofile(self):
        """
        Test that a user can record a new profile, and that the proper data is grabbed 
        and rendered on the chart via polling.
        """       

        self.selenium.get(
            '%s%s' % (
                self.live_server_url, 
                reverse('roastprofile-detail', args=(self.roastprofile.id,))
            )
        )

        self.selenium.find_element_by_id("listen-newprofile").click()

        waiting = True    
        timeout = 10
        count = 0
        while waiting:
            try: 
                new_rp = models.RoastProfile.objects.exclude(id=self.roastprofile.id).get()
                waiting = False
            except models.RoastProfile.DoesNotExist as e:
                if count > timeout:
                    raise e
                time.sleep(1)
            count += 1
        waiting = None

        for i in range(30):
            models.TempPoint.objects.create(
                roast_profile=new_rp, 
                time=str(i+1), 
                temperature='%s.1' % (str(i*5))
            )

        # assert that all the points were rendered

        # The script will take at least 5 seconds before it will grab the data and render it.
        time.sleep(5)

        waiting = True
        timeout = 10
        count = 0
        while waiting:
            try:
                for index, point in enumerate(new_rp.temppoint_set.all()):
                    self.selenium.find_element_by_css_selector(
                        "g.nv-group.nv-series-1 .nv-point-%s" % index
                    ).click()
                waiting = False
            except NoSuchElementException as e:
                if count > timeout:
                    raise e
                time.sleep(1)
            count += 1
        waiting = None

        self.selenium.find_element_by_id("listen-newprofile").click()


class TestAjaxViews(TestCase):
    """
    Test that every API route that will be called via JS AJAX will work as expected.
    """

    def setUp(self):
        self.coffee = CoffeeFactory.create()
        self.coffee._generate_profile()
        self.roastprofile = self.coffee.roastprofile_set.all()[0]
        self.request_factory = RequestFactory()
        self.api_request_factory = APIRequestFactory()

    def tearDown(self):
        self.coffee.delete()

    def test_temppoint_comment_create_form(self):
        """
        Test that this view properly responds with a rendered form as JSON.
        """

        some_temppoint = self.roastprofile.temppoint_set.all()[0]
        request = self.api_request_factory.get(
            reverse('rest-pointcomment-get-form'), 
            {'id': some_temppoint.id }
        )

        view = views.PointCommentViewSet.as_view(actions={'get':'get_form'})

        response = view(request, pk=some_temppoint.id)

        data = render_to_string(
            '_includes/forms/point_comment_form.jade',
            {
                'point': some_temppoint,
                'form': forms.PointCommentForm(data={'point':some_temppoint.id}),
                'comments': some_temppoint.pointcomment_set.all().order_by('created')
            }
        )
        expected_response = JsonResponse({'data':data})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected_response.content)

    def test_temppoint_comment_create(self):
        """
        Test that this view properly creates a comment on the temppoint.
        """

        some_temppoint = self.roastprofile.temppoint_set.all()[0]
        comment = 'I made a comment dood'

        request = self.api_request_factory.post(
            reverse('rest-pointcomment-list',),
            {'point':some_temppoint.id, 'comment': comment},
        )

        view = views.PointCommentViewSet.as_view(actions={'post':'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        comment_queryset = models.PointComment.objects.filter(point__id=some_temppoint.id, comment=comment)
        self.assertEqual(comment_queryset.exists(), True)
        self.assertEqual(comment_queryset.count(), 1)

    def test_comment_delete(self):
        """
        Test that this view deletes a PointComment based on it's ID, and returns appropriate data 
        for the JavaScript to use.
        """

        some_temppoint = self.roastprofile.temppoint_set.all()[0]
        pointcomment = factories.PointCommentFactory.create(point=some_temppoint, comment="Hay")

        request = self.api_request_factory.delete(
            reverse(
                'rest-pointcomment-delete-and-respond',
                kwargs={'pk':pointcomment.id},
            )
        )

        self.assertEqual(models.PointComment.objects.filter(id=pointcomment.id).exists(), True)

        view = views.PointCommentViewSet.as_view(actions={'delete':'delete_and_respond'})

        response = view(request, pk=pointcomment.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"deletedCommentID": %s, "hasComments": false}' % pointcomment.id)
        self.assertEqual(models.PointComment.objects.filter(id=pointcomment.id).exists(), False)

    def test_roastprofile_create(self):
        """
        Test that this view creates a new RoastProfile with a Coffee as it's parent based 
        on that Coffee's ID.
        """

        request = self.api_request_factory.post(
            reverse('rest-roastprofile-list'),
            {'coffee': self.coffee.id, 'name': 'Test Profile'}
        )

        self.assertEqual(self.coffee.roastprofile_set.all().count(), 1)

        view = views.RoastProfileViewSet.as_view(actions={'post':'create'})

        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.coffee.roastprofile_set.all().count(), 2)

    def test_roastprofile_delete(self):
        """
        Test that this view delete's a RoastProfile based on it's ID.
        """

        request = self.api_request_factory.delete(
            reverse(
                'rest-roastprofile-detail',
                kwargs={'pk': self.roastprofile.id}
            )
        )

        self.assertEqual(self.coffee.roastprofile_set.all().count(), 1)

        view = views.RoastProfileViewSet.as_view(actions={'delete':'destroy'})

        response = view(request, pk=self.roastprofile.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.coffee.roastprofile_set.all().exists(), False)

    def test_roastprofile_graph_data(self):
        """
        Test that this view properly returns a JSON response with 'graphData' that is 
        a JSON encoded form of a RoastProfile's get_temp_graph_data method.
        """

        request = self.api_request_factory.get(
            reverse(
                'rest-roastprofile-detail',
                kwargs={'pk': self.roastprofile.id}
            )
        )

        view = views.RoastProfileViewSet.as_view(actions={'get':'retrieve'})

        response = view(request, pk=self.roastprofile.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['temp_graph_data'], 
            self.roastprofile._get_temp_graph_data()
        )

    def test_roastprofile_graph_data_slice(self):
        """
        Test that this view properly returns a slice of a set of related TempPoints from a RoastProfile.
        """

        slice_start = '5'
        request = self.api_request_factory.get(
            reverse('rest-roastprofile-get-graph-data-slice'),
            {
                'id': self.roastprofile.id,
                'sliceStart': slice_start
            }
        )

        view = views.RoastProfileViewSet.as_view(actions={'get':'get_graph_data_slice'})
        
        response = view(request)

        expected_data = {
            'graphDataValues': self.roastprofile.get_temp_graph_data_slice(slice_start),
            'lastSlice': self.roastprofile.temppoint_set.all().order_by('-time')[0].time
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, JsonResponse(expected_data).content)