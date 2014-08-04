# Django
from django.db import models

# Third Party
from django_extensions.db.models import TimeStampedModel
import pytz
import simplejson

# Python
import datetime
import random


class RoastProfile(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    date = models.DateTimeField(default=datetime.datetime.utcnow())
    coffee = models.ForeignKey('coffee.Coffee', null=True, blank=False)

    def get_temp_graph_data_JSON(self):
    	"""
    	This method grabs all of the associated TempPoints for this RoastProfile,
    	and formats them into a suitable data structure for a d3 line chart, as JSON.
    	It is intended to be used on the template, to directly drop in data for a line chart.
    	"""
        data = []
        if self.temppoint_set.all().exists():
            temp_points = self.temppoint_set.all().order_by('time')
            values_list = []
            for temp_point in temp_points:
                values_list.append(
                    {
                    'x':temp_point.time,
                    'y':float(temp_point.temperature), 
                    'id': temp_point.id,
                    'hasComments': temp_point.pointcomment_set.all().exists(),
                    }
                )
            data.append(
                {
                'values': values_list,
                'key': self.name,
                }
            )

        return simplejson.dumps(data)

    def get_pointcomment_count(self):
        # TODO: Make this more efficient
        count = 0
        for temppoint in self.temppoint_set.all().prefetch_related('pointcomment_set'):
            if temppoint.pointcomment_set.all().exists():
                count += temppoint.pointcomment_set.all().count()
        return count

    def __unicode__(self):
        if self.coffee:
            return u'%s - %s' % (self.coffee, self.name)
        else:
            return self.name

    class Meta:
        verbose_name = 'Roast Profile'
        verbose_name_plural = 'Roast Profiles'


class TempPoint(models.Model):
    temperature = models.CharField(max_length=255, null=False, default=u'212.0')
    time = models.PositiveIntegerField()
    roast_profile = models.ForeignKey('log.RoastProfile', null=False)

    def __unicode__(self):
        if self.roast_profile.coffee:
            return u'%s - %s - %s - %s' % (
                self.roast_profile.coffee.name, 
                self.roast_profile, 
                unicode(self.time), 
                self.temperature
            )
        else:
            return u'%s - %s - %s' % (self.roast_profile, unicode(self.time), self.temperature)

    class Meta:
        verbose_name = 'Temperature Point'
        verbose_name_plural = 'Temperature Points'


class PointComment(TimeStampedModel):
    point = models.ForeignKey('log.TempPoint', null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    # author = models.ForeignKey