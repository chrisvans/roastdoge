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
    harvest_date = models.DateTimeField(auto_now_add=True)
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
        from profiling.models import RoastProfile, TempPoint

        profile = RoastProfile.objects.create(
            coffee=self, 
            name=u'%s - %s' % (self.name, str(RoastProfile.objects.all().count()+1)),
        )
        drop_temp = random.choice([u'220.0', u'230.0', u'215.0', u'205.0', u'208.0'])
        start_temp = u'80.0'

        low_temp = 80
        degreerangeintslow = range(1, 3)
        degreerangeintmed = range(2, 4)
        degreerangeintramp = range(10, 15) 
        degreerangedec = range(10)
        breakpoint = {
            '0':214,
            '1':206,
            '2':208,
            '3':210,
            '4':212,
        }[random.choice(['0', '1', '2', '3', '4',])]

        temp = drop_temp

        for i in range(60):

            templist = temp.split('.')

            temp = u'%s.%s' % (
                str(int(templist[0]) - random.choice(degreerangeintramp)),
                str(int(templist[1]) + random.choice(degreerangedec))
            )

            if int(temp.split('.')[0]) < (low_temp):
                last_temp = i
                break    

            TempPoint.objects.create(
                temperature=temp,
                time=i,
                roast_profile=profile
            )

        temp = start_temp

        for i in range(3):

            templist = temp.split('.')

            if i == 1:
                temp = u'%s.%s' % (
                    str(int(templist[0])),
                    str(int(templist[1])),
                )
            elif i == 2:
                temp = u'%s.%s' % (
                    str(int(templist[0])),
                    str(int(templist[0]) + 1),
                )
            else:
                temp = u'%s.%s' % (
                    str(int(templist[0]) + 1),
                    str(int(templist[0]) + 2),
                )

            TempPoint.objects.create(
                temperature=temp,
                time=last_temp + i,
                roast_profile=profile
            )  

            last_temp += (i+1)

        for i in range(1000):

            templist = temp.split('.')

            if i < 5:
                temp = u'%s.%s' % (
                    str(int(templist[0]) + random.choice(degreerangeintmed)),
                    str(int(templist[1]) + random.choice(degreerangedec))
                )
            else:
                temp = u'%s.%s' % (
                    str(int(templist[0]) + random.choice(degreerangeintslow)),
                    str(int(templist[1]) + random.choice(degreerangedec))
                )

            if int(temp.split('.')[0]) > (breakpoint):
                break  

            TempPoint.objects.create(
                temperature=temp,
                time=last_temp + i,
                roast_profile=profile
            )   

    def __unicode__(self):
        return self.name