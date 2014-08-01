# Django
from django import forms

# Ours
import models


class PointCommentForm(forms.ModelForm):

    class Meta:
        model = models.PointComment