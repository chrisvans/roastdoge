# Django
from django import forms

# Ours
import models


class PointCommentForm(forms.ModelForm):

    class Meta:
        model = models.PointComment


class RoastProfileSelectForm(forms.Form):

	roastprofile_select = forms.ModelChoiceField(queryset=models.RoastProfile.objects.all())


class RoastProfileForm(forms.ModelForm):

    class Meta:
        model = models.RoastProfile