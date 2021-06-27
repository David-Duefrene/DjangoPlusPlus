"""Allows the ability to create various Users for testing purposes."""
from django.contrib.auth.models import User

from faker import Faker
import random


def create_user(model=User):
    """Create a new user in the test DB."""
    generator = Faker()
    full_name = generator.name()
    full_name = full_name.split()
    username = full_name[0] + full_name[1] + str(random.randint(0, 1000))

    user = model.objects.create(
        username=username,
        email=f'{username}@test.com',
        first_name=full_name[0],
        last_name=full_name[1],
    )

    user.set_password('password')
    user.save()

    return user
