# Third Party
from rest_framework import serializers
import simplejson

# Ours
import models


class JSONSourceField(serializers.WritableField):
    """
    This field serializer is intended to be used on a textfield or jsonfield that
    stores JSON.  The data stored in this field should already be in JSON, and so 
    does not need to be modified any further.
    """

    def to_native(self, obj):
        return simplejson.loads(obj)


class TempPointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TempPoint
        fields = ('temperature', 'time', )


class RoastProfileSerializer(serializers.HyperlinkedModelSerializer):

    temppoint = TempPointSerializer(read_only=True, source="temppoint_set")
    _graph_data_cache = JSONSourceField(read_only=True, source='_graph_data_cache')

    class Meta:
        model = models.RoastProfile
        fields = ('name', 'date', '_graph_data_cache', 'temppoint',)