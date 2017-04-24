import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = factory.Sequence(lambda n: 'User_%s' % n)
    last_name = factory.Sequence(lambda n: 'User_%s' % n)
    email = factory.LazyAttribute(lambda o: '%s@gmail.com' % o.first_name)
