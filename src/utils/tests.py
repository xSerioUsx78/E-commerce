from django.contrib.auth import get_user_model
from django.test import TestCase as BaseTestCase


User = get_user_model()


class TestCase(BaseTestCase):

    def setUp(self):
        self.superuser = User.objects.create_user(
            username="superuser",
            password="superuser",
            is_staff=True,
            is_superuser=True
        )
        self.staff = User.objects.create_user(
            username="staff",
            password="staff",
            is_staff=True
        )
        self.user = User.objects.create_user(
            username="user",
            password="user"
        )

    def authenticate(self, user=None):
        if not user:
            user = self.user
        self.client.force_login(user)
