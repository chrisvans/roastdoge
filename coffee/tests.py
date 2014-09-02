# Django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.test import TestCase, Client, RequestFactory

# Ours
import factories
import models
import ajax
import forms

# Third Party
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import ui

# Python
import time

# TODO: Create functional tests for the listviews' (RoastProfile, Coffee) delete action

class TestAjaxViews(TestCase):

    def setUp(self):
        self.coffee = factories.CoffeeFactory.create()
        self.coffee._generate_profile()
        self.roastprofile = self.coffee.roastprofile_set.all()[0]
        self.request_factory = RequestFactory()

    def tearDown(self):
        self.coffee.delete()

    def test_coffee_delete(self):
        """
        Test that this view properly deletes a Coffee based on it's ID
        """

        request = self.request_factory.post(
            reverse('ajax-coffee-delete'),
            {'coffeeID': self.coffee.id},
        )

        self.assertEquals(models.Coffee.objects.filter(id=self.coffee.id).exists(), True)
        
        response = ajax.coffee_delete(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(models.Coffee.objects.filter(id=self.coffee.id).exists(), False)

