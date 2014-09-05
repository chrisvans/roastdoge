# Third Party
from rest_framework import serializers

# Ours
import models
import profiling


class CoffeeSerializer(serializers.HyperlinkedModelSerializer):

    roastprofile_set = profiling.serializers.RoastProfileSerializer(read_only=True, source='roastprofile_set')

    class Meta:
        model = models.Coffee
        fields = ('name', 'roastprofile_set', )
