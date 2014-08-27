# Ours
import models

# Third Party
import factory


class CoffeeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Coffee

    name = factory.Sequence(lambda n: 'Test Coffee {0}'.format(n))