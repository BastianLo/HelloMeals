from django.contrib.auth.models import User
from rest_framework.test import APIClient


def create_user(username, password="test-pass-123", is_staff=False, is_superuser=False):
    user = User.objects.create_user(username=username, password=password)
    if is_staff or is_superuser:
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
    return user


def create_admin(username="admin"):
    return create_user(username, is_staff=True, is_superuser=True)


def authenticated_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client
