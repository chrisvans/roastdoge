# Django
from django import forms
from django.forms import extras

# Ours
import models as roastdoge_models

# Python
import datetime


POSSIBLE_YEARS = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
YEARS = [year for year in POSSIBLE_YEARS if year <= datetime.datetime.now().year]


class GreenCoffeeForm(forms.ModelForm):

    class Meta:
        model = roastdoge_models.GreenCoffee
        widgets = { 'harvest_date': extras.SelectDateWidget(years=YEARS) }


class CoffeeForm(forms.ModelForm):

    class Meta:
        model = roastdoge_models.Coffee
        # TODO - Add a widget for selecting multiple coffee components