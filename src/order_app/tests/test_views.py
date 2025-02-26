from rest_framework import status

from utils.tests import APITestCase
from product_app.models import Product, ProductVariation, ProductVariationItem
from order_app.models import Order, OrderItem
from address_app.models import Address


class OrderItemTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.base_url = "/api/order/item/"

        self.product1 = Product.objects.create(
            user=self.superuser,
            price=1000
        )
        self.product2 = Product.objects.create(
            user=self.superuser,
            price=2000
        )

    def test_add_product_without_variation(self):
        """
        Steps:
            Step 1: we add a product in order and check the order item quantity is 1.
            Step 2: we add that product again in order and check the order item quantity has increased and it's 2.
            Step 3: we add another product and check the quantity of those two order items are correct.
        """

        self.authenticate(self.user)
        url = f'{self.base_url}action/'
        data = {
            "product_id": self.product1.id,
            "action": "add"
        }

        # STEP 1
        res1 = self.client.post(
            url,
            data
        )
        self.assertTrue(res1.status_code == status.HTTP_200_OK)

        json1 = res1.json()

        self.assertIn("message", json1)
        self.assertIn("order_item_id", json1)

        order_item = OrderItem.objects.get(id=json1['order_item_id'])

        self.assertEqual(order_item.quantity, 1)
        self.assertTrue(order_item.order)
        self.assertTrue(order_item.product_variation_items.count() == 0)

        # STEP 2
        res2 = self.client.post(
            url,
            data
        )
        self.assertTrue(res2.status_code == status.HTTP_200_OK)

        json2 = res2.json()

        self.assertIn("message", json2)
        self.assertIn("order_item_id", json2)

        order_item.refresh_from_db()

        self.assertEqual(order_item.quantity, 2)
        self.assertTrue(order_item.order)
        self.assertTrue(order_item.product_variation_items.count() == 0)

        # STEP 3
        data2 = {
            "product_id": self.product2.id,
            "action": "add"
        }
        res3 = self.client.post(
            url,
            data2
        )
        self.assertTrue(res3.status_code == status.HTTP_200_OK)

        json3 = res3.json()

        self.assertIn("message", json3)
        self.assertIn("order_item_id", json3)

        order_item2 = OrderItem.objects.get(id=json3['order_item_id'])

        self.assertEqual(order_item2.quantity, 1)
        self.assertTrue(order_item2.order)
        self.assertTrue(order_item2.product_variation_items.count() == 0)

    def test_add_product_with_variation(self):
        """
        Steps:
            Step 2: Create product variation and variation item for each product and assign it to them.
            Step 2: Add a product in order and check the order item quantity is 1.
            Step 3: Add that product again in order and check the order item quantity has increased and it's 2.
            Step 4: Add that product again with different variation item and check the order item quantity is 1.
            Step 5: Add another product and check the quantity of those two order items are correct.
        """

        self.authenticate(self.user)
        url = f'{self.base_url}action/'

        # Step 1
        product1_variation1 = ProductVariation.objects.create(
            user=self.superuser,
            product=self.product1,
            title="Variation 1"
        )
        product1_variation_item1 = ProductVariationItem.objects.create(
            user=self.superuser,
            product_variation=product1_variation1,
            name="Name 1",
            value="Value 1",
            price=80
        )
        product1_variation_item2 = ProductVariationItem.objects.create(
            user=self.superuser,
            product_variation=product1_variation1,
            name="Name 2",
            value="Value 2",
            price=90
        )

        product2_variation = ProductVariation.objects.create(
            user=self.superuser,
            product=self.product2,
            title="Variation 2"
        )
        product2_variation_item1 = ProductVariationItem.objects.create(
            user=self.superuser,
            product_variation=product2_variation,
            name="Name 3",
            value="Value 3",
            price=100
        )

        # STEP 2
        data = {
            "product_id": self.product1.id,
            "product_variation_items_id": [product1_variation_item1.id],
            "action": "add"
        }
        res1 = self.client.post(
            url,
            data
        )

        self.assertTrue(res1.status_code == status.HTTP_200_OK)

        json1 = res1.json()

        self.assertIn("message", json1)
        self.assertIn("order_item_id", json1)

        order_item = OrderItem.objects.get(id=json1['order_item_id'])

        self.assertEqual(order_item.quantity, 1)
        self.assertTrue(order_item.order)
        self.assertTrue(order_item.product_variation_items)

        # STEP 3
        res2 = self.client.post(
            url,
            data
        )
        self.assertTrue(res2.status_code == status.HTTP_200_OK)

        json2 = res2.json()

        self.assertIn("message", json2)
        self.assertIn("order_item_id", json2)

        order_item.refresh_from_db()

        self.assertEqual(order_item.quantity, 2)
        self.assertTrue(order_item.order)
        self.assertTrue(order_item.product_variation_items)

        # STEP 4
        data2 = {
            "product_id": self.product1.id,
            "product_variation_items_id": [product1_variation_item2.id],
            "action": "add"
        }
        res3 = self.client.post(
            url,
            data2
        )
        self.assertTrue(res3.status_code == status.HTTP_200_OK)

        json3 = res3.json()

        self.assertIn("message", json3)
        self.assertIn("order_item_id", json3)

        order_item2 = OrderItem.objects.get(id=json3['order_item_id'])

        self.assertEqual(order_item2.quantity, 1)
        self.assertTrue(order_item2.order)
        self.assertTrue(order_item2.product_variation_items)

        # STEP 5
        data4 = {
            "product_id": self.product2.id,
            "product_variation_items_id": [product2_variation_item1.id],
            "action": "add"
        }
        res4 = self.client.post(
            url,
            data4
        )
        self.assertTrue(res4.status_code == status.HTTP_200_OK)

        json4 = res4.json()

        self.assertIn("message", json4)
        self.assertIn("order_item_id", json4)

        order_item2 = OrderItem.objects.get(id=json4['order_item_id'])

        self.assertEqual(order_item2.quantity, 1)
        self.assertTrue(order_item2.order)
        self.assertTrue(order_item2.product_variation_items)

    def test_remove_product_without_variation(self):
        """
        Steps:
            Step 1: Create an order and order item for the user.
            Step 2: Send a request to decrease the quantity of the product from the order.
            Step 3: Send a request again to remove the product from the order.
        """

        self.authenticate(self.user)
        url = f'{self.base_url}action/'

        # STEP 1
        order, _ = Order.objects.get_or_create(user=self.user)
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product1,
            quantity=2
        )

        # STEP 2
        data = {
            "product_id": self.product1.id,
            "action": "remove"
        }
        res = self.client.post(
            url,
            data
        )
        self.assertTrue(res.status_code == status.HTTP_200_OK)

        order_item.refresh_from_db()

        self.assertTrue(order_item.quantity == 1)

        # STEP 3
        data2 = {
            "product_id": self.product1.id,
            "action": "remove"
        }
        res2 = self.client.post(
            url,
            data2
        )
        self.assertTrue(res2.status_code == status.HTTP_200_OK)
        self.assertTrue(OrderItem.objects.count() == 0)

    def test_remove_product_with_variation(self):
        """
        Steps:
            Step 1: Create an order and order item for the user.
            Step 2: Send a request to decrease the quantity of the product from the order.
            Step 3: Send a request again to remove the product from the order.
        """

        self.authenticate(self.user)
        url = f'{self.base_url}action/'

        # STEP 1
        order, _ = Order.objects.get_or_create(user=self.user)
        product_variation = ProductVariation.objects.create(
            user=self.superuser,
            product=self.product1,
            title="Variation 1"
        )
        product_variation_item = ProductVariationItem.objects.create(
            user=self.superuser,
            product_variation=product_variation,
            name="Name 1",
            value="Value 1",
            price=80
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product1,
            quantity=2
        )
        order_item.product_variation_items.add(product_variation_item)

        # STEP 2
        data = {
            "product_id": self.product1.id,
            "product_variation_items_id": product_variation_item.id,
            "action": "remove"
        }
        res = self.client.post(
            url,
            data
        )
        self.assertTrue(res.status_code == status.HTTP_200_OK)

        order_item.refresh_from_db()

        self.assertTrue(order_item.quantity == 1)

        # STEP 3
        data2 = {
            "product_id": self.product1.id,
            "product_variation_items_id": [product_variation_item.id],
            "action": "remove"
        }
        res2 = self.client.post(
            url,
            data2
        )
        self.assertTrue(res2.status_code == status.HTTP_200_OK)
        self.assertTrue(OrderItem.objects.count() == 0)

    def test_perform_action_bad_action(self):
        """
        Steps:
            Step 1: Send request to perform action with bad action.
        """

        self.authenticate(self.user)
        url = f'{self.base_url}action/'

        # STEP 1
        data = {
            "product_id": self.product1.id,
            "action": "bad_action"
        }
        res = self.client.post(
            url,
            data
        )
        self.assertTrue(res.status_code == status.HTTP_400_BAD_REQUEST)

    def test_perform_action_bad_product_id(self):
        """
        Steps:
            Step 1: Send request to perform action with bad product id.
        """

        self.authenticate(self.user)
        url = f'{self.base_url}action/'

        # STEP 1
        data = {
            "product_id": 0,
            "action": "add"
        }
        res = self.client.post(
            url,
            data
        )
        self.assertTrue(res.status_code == status.HTTP_400_BAD_REQUEST)

    def test_perform_action_wrong_product_id(self):
        """
        Steps:
            Step 1: Send request to perform action with wrong product id.
        """

        self.authenticate(self.user)
        url = f'{self.base_url}action/'

        # STEP 1
        data = {
            "product_id": 100,
            "action": "add"
        }
        res = self.client.post(
            url,
            data
        )
        self.assertTrue(res.status_code == status.HTTP_400_BAD_REQUEST)

    def test_perform_action_bad_product_variation_id(self):
        """
        Steps:
            Step 1: Send request to perform action with bad product variation item id.
        """

        self.authenticate(self.user)
        url = f'{self.base_url}action/'

        # STEP 1
        data = {
            "product_id": self.product1.id,
            "product_variation_items_id": [0],
            "action": "add"
        }
        res = self.client.post(
            url,
            data
        )
        self.assertTrue(res.status_code == status.HTTP_400_BAD_REQUEST)

    def test_perform_action_wrong_product_variation_id(self):
        """
        Steps:
            Step 1: Send request to perform action with wrong product variation item id.
        """

        self.authenticate(self.user)
        url = f'{self.base_url}action/'

        # STEP 1
        data = {
            "product_id": self.product1.id,
            "product_variation_items_id": [100],
            "action": "add"
        }
        res = self.client.post(
            url,
            data
        )
        self.assertTrue(res.status_code == status.HTTP_400_BAD_REQUEST)

    def test_perform_action_product_variation_id_for_different_product(self):
        """
        Steps:
            Step 1: Create product variation and product variation item for different product.
            Step 2: Send a request to perform action with product 2 and product variation item that set for product 1.
        """

        self.authenticate(self.user)
        url = f'{self.base_url}action/'

        # STEP 1
        product_variation = ProductVariation.objects.create(
            user=self.superuser,
            product=self.product1,
            title="Variation 1"
        )
        product_variation_items = ProductVariationItem.objects.create(
            user=self.superuser,
            product_variation=product_variation,
            name="Name 1",
            value="Value 1",
            price=80
        )

        # STEP 2
        data = {
            "product_id": self.product2.id,
            "product_variation_items_id": [product_variation_items.id],
            "action": "remove"
        }
        res = self.client.post(
            url,
            data
        )
        self.assertTrue(res.status_code == status.HTTP_400_BAD_REQUEST)


class OrderTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.base_url = "/api/order/"

        self.product1 = Product.objects.create(
            user=self.superuser,
            price=10
        )
        self.product2 = Product.objects.create(
            user=self.superuser,
            price=20
        )
        product1_variation1 = ProductVariation.objects.create(
            user=self.superuser,
            product=self.product1,
            title="Variation 1"
        )
        product1_variation2 = ProductVariation.objects.create(
            user=self.superuser,
            product=self.product1,
            title="Variation 1"
        )
        self.product1_variation_item1 = ProductVariationItem.objects.create(
            user=self.superuser,
            product_variation=product1_variation1,
            name="Name 1",
            value="Value 1",
            price=1
        )
        self.product1_variation_item2 = ProductVariationItem.objects.create(
            user=self.superuser,
            product_variation=product1_variation2,
            name="Name 2",
            value="Value 2",
            price=2
        )

        product2_variation = ProductVariation.objects.create(
            user=self.superuser,
            product=self.product2,
            title="Variation 2"
        )
        self.product2_variation_item1 = ProductVariationItem.objects.create(
            user=self.superuser,
            product_variation=product2_variation,
            name="Name 3",
            value="Value 3",
            price=3
        )

    def test_order_list(self):

        self.authenticate(self.user)
        url = f'{self.base_url}cart/'

        order, _ = Order.objects.get_or_create(user=self.user)
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product1,
            quantity=2
        )
        order_item.product_variation_items.set([
            self.product1_variation_item1,
            self.product1_variation_item2
        ])

        res = self.client.get(url)

        self.assertTrue(res.status_code == status.HTTP_200_OK)

        json = res.json()

        self.assertIn('total_price_calculated', json)
        self.assertIn('total_discount_calculated', json)
        self.assertIn('items', json)
        self.assertTrue(json['total_price_calculated'] == 26.0)

        items = json['items']

        for item in items:
            self.assertIn("product", item)
            self.assertIn("product_variation_items", item)
            self.assertIn("quantity", item)

            product_variation_items = item['product_variation_items']

            for product_variation_item in product_variation_items:
                self.assertIn("product_variation", product_variation_item)
                self.assertIn("name", product_variation_item)
                self.assertIn("value", product_variation_item)

                product_variation = product_variation_item['product_variation']
                self.assertIn('title', product_variation)

    def test_create_payment_link_success(self):
        self.authenticate(self.user)

        url = f'{self.base_url}create-payment-link/'

        Order.objects.create(user=self.user)
        address = Address.objects.create(user=self.user)

        data = {
            "address": address.pk,
            "method": "zarinpal"
        }

        res = self.client.post(
            url,
            data
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_200_OK
        )
        json = res.json()
        self.assertIn('payment_link', json)
