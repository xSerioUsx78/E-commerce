from rest_framework import status

from utils.tests import APITestCase
from address_app.models import Address


class AddressAPITestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.base_url = "/api/address/"

    def test_address_list(self):
        self.authenticate(self.user)

        Address.objects.create(
            user=self.user
        )
        Address.objects.create(
            user=self.user
        )
        Address.objects.create(
            user=self.user2
        )

        res = self.client.get(self.base_url)

        self.assertTrue(res.status_code == status.HTTP_200_OK)

        json = res.json()

        self.assertIn('count', json)
        self.assertIn('next', json)
        self.assertIn('previous', json)
        self.assertIn('results', json)

        self.assertTrue(json['count'] == 2)

        results = json['results']
        for obj in results:
            self.assertIn("province", obj)
            self.assertIn("city", obj)
            self.assertIn("address", obj)
            self.assertIn("plaque", obj)
            self.assertIn("unit", obj)
            self.assertIn("postal_code", obj)
            self.assertIn("default", obj)

    def test_address_create_success(self):
        self.authenticate(self.user)

        data = {
            "province": "province",
            "city": "city",
            "address": "address",
            "plaque": "plaque",
            "unit": "unit",
            "postal_code": "postal_code",
            "default": True  # Read only
        }

        res = self.client.post(
            self.base_url,
            data
        )

        self.assertTrue(res.status_code == status.HTTP_201_CREATED)

        queryset = Address.objects.filter(
            user=self.user
        )

        self.assertTrue(queryset.count(), 1)

        address = queryset.first()

        self.assertEqual(address.province, data['province'])
        self.assertEqual(address.city, data['city'])
        self.assertEqual(address.address, data['address'])
        self.assertEqual(address.plaque, data['plaque'])
        self.assertEqual(address.unit, data['unit'])
        self.assertEqual(address.postal_code, data['postal_code'])

        """
        Default is read only, even if we pass a True value,
        it should remain False.
        """
        self.assertEqual(address.default, False)

    def test_address_update_success(self):
        self.authenticate(self.user)

        address = Address.objects.create(
            user=self.user,
            province="Test",
            city="Test",
            address="Test",
            plaque="Test",
            unit="Test",
            postal_code="Test"
        )

        data = {
            "province": "province",
            "city": "city",
            "address": "address",
            "plaque": "plaque",
            "unit": "unit",
            "postal_code": "postal_code",
            "default": True  # Read only
        }

        url = f'{self.base_url}{address.pk}/'
        res = self.client.put(
            url,
            data=data
        )

        self.assertTrue(res.status_code == status.HTTP_200_OK)

        address.refresh_from_db()

        self.assertEqual(address.province, data['province'])
        self.assertEqual(address.city, data['city'])
        self.assertEqual(address.address, data['address'])
        self.assertEqual(address.plaque, data['plaque'])
        self.assertEqual(address.unit, data['unit'])
        self.assertEqual(address.postal_code, data['postal_code'])

        """
        Default is read only, even if we pass a True value,
        it should remain False.
        """
        self.assertEqual(address.default, False)

    def test_address_delete_success(self):
        self.authenticate(self.user)

        address = Address.objects.create(
            user=self.user
        )
        Address.objects.create(
            user=self.user2
        )

        url = f'{self.base_url}{address.pk}/'

        res = self.client.delete(
            url
        )

        self.assertTrue(res.status_code == status.HTTP_204_NO_CONTENT)
        self.assertFalse(Address.objects.filter(user=self.user).exists())
        self.assertTrue(Address.objects.count() == 1)

    def test_address_make_default(self):
        self.authenticate(self.user)

        address = Address.objects.create(
            user=self.user,
            default=True
        )
        address2 = Address.objects.create(
            user=self.user,
            default=False
        )

        url = f'{self.base_url}{address2.pk}/make-default/'

        res = self.client.put(
            url
        )
        self.assertTrue(res.status_code == status.HTTP_204_NO_CONTENT)

        address.refresh_from_db()
        address2.refresh_from_db()

        self.assertFalse(address.default)
        self.assertTrue(address2.default)
