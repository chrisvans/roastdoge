# Third Party
from django.contrib.auth.models import User, Group
from rest_framework import serializers

# Ours
import models


class RoastProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RoastProfile
        fields = ('name', 'date', '_graph_data_cache', )


class TempPointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TempPoint
        fields = ('temperature', 'time', )