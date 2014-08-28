# Ours
import models

# Python
import datetime

# Third Party
import factory


class RoastProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.RoastProfile

    name = factory.Sequence(lambda n: 'Profile de Cafe {0}'.format(n))
    date = datetime.datetime.utcnow()
    coffee = factory.SubFactory('coffee.factories.CoffeeFactory')


class TempPointFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.TempPoint

    time = factory.Sequence(lambda n: '{0}'.format(n))
    temperature = factory.Sequence(lambda n: '{0}.2'.format(n+80))
    roast_profile = factory.SubFactory(RoastProfileFactory)
