# Third Party
from rest_framework import serializers
import simplejson

# Ours
import models


class PointCommentSerializer(serializers.HyperlinkedModelSerializer):

    point = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = models.PointComment
        fields = ('id', 'comment', 'point', )


class RoastProfileSerializer(serializers.HyperlinkedModelSerializer):

    coffee = serializers.PrimaryKeyRelatedField()
    date = serializers.DateTimeField(read_only=True)
    temp_graph_data = serializers.SerializerMethodField('get_temp_graph_data')

    def get_temp_graph_data(self, obj):
        return obj._get_temp_graph_data()

    class Meta:
        model = models.RoastProfile
        fields = ('id', 'coffee', 'name', 'date', 'temp_graph_data',)


class TempPointSerializer(serializers.HyperlinkedModelSerializer):

    roast_profile = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = models.TempPoint
        fields = ('id', 'temperature', 'time', 'roast_profile', )

