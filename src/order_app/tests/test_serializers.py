from utils.tests import APITestCase
from order_app.models import Order
from address_app.models import Address
from order_app.serializers import OrderCreatePaymentLinkSerializer


class OrderCreatePaymentLinkSerializerTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.order = Order.objects.create(
            user=self.user
        )
        self.address = Address.objects.create(
            user=self.user
        )
        self.address2 = Address.objects.create(
            user=self.user2
        )
        self.serializer = OrderCreatePaymentLinkSerializer

    def test_field_validation_bad_address_lower_than_min_value(self):
        data = {
            "address": 0,
            "method": "zarinpal"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("address", errors)

    def test_field_validation_bad_address_not_exists_address_id(self):
        request = self.client.get('/')
        request.user = self.user

        data = {
            "address": 10,
            "method": "zarinpal"
        }
        serializer = self.serializer(
            data=data,
            context={"request": request}
        )
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("address", errors)

    def test_field_validation_bad_address_another_user_address_id(self):
        request = self.client.get('/')
        request.user = self.user

        data = {
            "address": self.address2.pk,
            "method": "zarinpal"
        }
        serializer = self.serializer(
            data=data,
            context={"request": request}
        )
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("address", errors)

    def test_field_validation_bad_method(self):
        data = {
            "address": self.address.pk,
            "method": "wrong"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("method", errors)

    def test_field_validation_no_method(self):
        data = {
            "address": self.address.pk,
            "method": ""
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("method", errors)

    def test_field_validation_no_order(self):
        request = self.client.get('/')
        request.user = self.user

        Order.objects.all().delete()

        data = {
            "address": self.address.pk,
            "method": "zarinpal"
        }
        serializer = self.serializer(
            data=data,
            context={"request": request}
        )
        self.assertFalse(serializer.is_valid())

    def test_field_validation_success(self):
        request = self.client.get('/')
        request.user = self.user

        data = {
            "address": self.address.pk,
            "method": "zarinpal"
        }
        serializer = self.serializer(
            data=data,
            context={"request": request}
        )
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)

    def test_field_validation_success_no_address(self):
        request = self.client.get('/')
        request.user = self.user

        data = {
            "address": None,
            "method": "zarinpal"
        }
        serializer = self.serializer(
            data=data,
            context={"request": request}
        )
        self.assertTrue(serializer.is_valid())
        errors = serializer.errors
        self.assertTrue(len(errors.keys()) == 0)

    def test_create_payment_link(self):
        request = self.client.get('/')
        request.user = self.user

        data = {
            "address": self.address.pk,
            "method": "zarinpal"
        }
        serializer = self.serializer(
            data=data,
            context={"request": request}
        )
        serializer.is_valid()
        res_data = serializer.create_payment_link()
        self.order.refresh_from_db()
        self.assertEqual(self.order.address, self.address)
        self.assertIn("payment_link", res_data)

    def test_create_payment_link_no_address(self):
        request = self.client.get('/')
        request.user = self.user

        data = {
            "address": None,
            "method": "zarinpal"
        }
        serializer = self.serializer(
            data=data,
            context={"request": request}
        )
        serializer.is_valid()
        res_data = serializer.create_payment_link()
        self.order.refresh_from_db()
        self.assertFalse(self.order.address)
        self.assertIn("payment_link", res_data)
