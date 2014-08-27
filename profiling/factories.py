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
