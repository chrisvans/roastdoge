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
    name = models.CharField(max_length=255, null=False, blank=False)
    date = models.DateTimeField(default=datetime.datetime.now)
    coffee = models.ForeignKey('coffee.Coffee', null=True, blank=False)
    _graph_data_cache = models.TextField(null=True, blank=True)

    def get_roastprofile_select_form(self):
        from forms import RoastProfileSelectForm
        form = RoastProfileSelectForm()
        form.fields['roastprofile_select'].queryset = form.fields['roastprofile_select'].queryset.exclude(id=self.id)
        return form

    def _get_temp_graph_data(self):
        """
        This method grabs all of the associated TempPoints for this RoastProfile,
        and formats them into a suitable data structure for a d3 line chart.
        """

        temp_points = self.temppoint_set.all().order_by('time').prefetch_related('pointcomment_set')
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
        data = {
            'values': values_list,
            'key': '%s %s' % (self.name, unicode(self.id) ),
            'id': self.id,
        }

        return data

    def get_temp_graph_data_JSON(self):
    	"""
    	This method grabs all of the associated TempPoints for this RoastProfile,
    	and formats them into a suitable data structure for a d3 line chart, as JSON.
    	It is intended to be used on the template, to directly drop in data for a line chart.
    	"""

        if not self._graph_data_cache:

            data = self._get_temp_graph_data()
            self._graph_data_cache = simplejson.dumps(data)
            self.save()

        return self._graph_data_cache

    def get_temp_graph_data_slice(self, start=False, end=False, get_comments=False):
        """
        Grabs a slice of temp points based on a start and end time.  Intended to be used
        when live updating a chart, to only grab the newest points.  If used otherwise,
        then pass get_comments in as True, otherwise hasComments will always return False.
        """
        temp_point_qs = self.temppoint_set.all().order_by('time')
        
        if start:
            temp_point_qs = temp_point_qs.filter(time__gte=start)
        if end:
            temp_point_qs = temp_point_qs.filter(time__lte=end)

        values_list = []

        if get_comments:
            for temp_point in temp_point_qs:
                values_list.append(
                    {
                    'x': temp_point.time,
                    'y': float(temp_point.temperature),
                    'id': temp_point.id,
                    'hasComments': False,
                    }
                )
        else:
            temp_point_qs = temp_point_qs.prefetch_related('pointcomment_set')
            for temp_point in temp_point_qs:
                values_list.append(
                    {
                    'x': temp_point.time,
                    'y': float(temp_point.temperature),
                    'id': temp_point.id,
                    'hasComments': temp_point.pointcomment_set.all().exists(),
                    }
                )            

        return values_list

    def get_pointcomment_count(self):
        # TODO: Make this more efficient
        count = 0
        for temppoint in self.temppoint_set.all().prefetch_related('pointcomment_set'):
            if temppoint.pointcomment_set.all().exists():
                count += temppoint.pointcomment_set.all().count()
        return count

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Roast Profile'
        verbose_name_plural = 'Roast Profiles'


class TempPoint(models.Model):
    # Default temp measurement is in C
    temperature = models.CharField(max_length=255, null=False, default=u'212.0')
    # Time is in seconds, relative to the start of the roast
    time = models.PositiveIntegerField()
    roast_profile = models.ForeignKey(RoastProfile, null=False)

    # TODO: Save this as a field on .save(), rather than processing on every str/uni eval.
    def __unicode__(self):
        return '%s %s' % (self.time, self.temperature)

    def get_detail_info(self):        
        if self.roast_profile.coffee:
            return u'%s - %s - %s - %s' % (
                self.roast_profile.coffee.name, 
                self.roast_profile, 
                unicode(self.time), 
                self.temperature
            )
        else:
            return u'%s - %s - %s' % (self.roast_profile, unicode(self.time), self.temperature)

    def save(self, *args, **kwargs):

        # Remove the cached graph_data on the roastprofile when a new point is saved.
        if self.id and self.roast_profile and self.roast_profile._graph_data_cache:
            self.roast_profile._graph_data_cache = None
            self.roast_profile.save()

        super(TempPoint, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Temperature Point'
        verbose_name_plural = 'Temperature Points'


class PointComment(TimeStampedModel):
    point = models.ForeignKey(TempPoint, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    # author = models.ForeignKey