from django.db import models

# Python
import datetime
import random


class GreenCoffee(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    country = models.CharField(max_length=255, null=True, blank=False)
    region = models.CharField(max_length=255, null=True, blank=True)
    farm = models.CharField(max_length=255, null=True, blank=True)
    varietal = models.CharField(max_length=255, null=True, blank=True)
    harvest_date = models.DateTimeField(default=datetime.datetime.utcnow())
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s' % (
            unicode(self.harvest_date), 
            self.name,
        )


class Coffee(models.Model):
    name = models.CharField(max_length=255, null=False)

    def _generate_profile(self):
        """
        Method for generating test profile data.
        """
        from log.models import RoastProfile, TempPoint

        profile = RoastProfile.objects.create(
            coffee=self, 
            name=u'%s - %s' % (self.name, str(RoastProfile.objects.all().count()+1)),
        )

        temp = u'80.0'
        degreerangeintslow = range(3, 7)
        degreerangeintramp = range(10, 15) 
        degreerangedec = range(10)
        breakpoint = {
            '0':214,
            '1':206,
            '2':208,
            '3':210,
            '4':212,
        }[str(profile.id % 5)]

        for i in range(25):

            TempPoint.objects.create(
                temperature=temp,
                time=i,
                roast_profile=profile
            )

            templist = temp.split('.')

            if i < 5:
                temp = u'%s.%s' % (
                    str(int(templist[0]) + random.choice(degreerangeintramp)),
                    str(int(templist[1]) + random.choice(degreerangedec))
                )
            else:
                temp = u'%s.%s' % (
                    str(int(templist[0]) + random.choice(degreerangeintslow)),
                    str(int(templist[1]) + random.choice(degreerangedec))
                )

            if int(temp.split('.')[0]) > (breakpoint):
                break       

    def __unicode__(self):
        return self.name