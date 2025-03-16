from rest_framework import status

from utils.tests import APITestCase
from product_app.models import Product
from question_answer_app.models import QuestionAnswer


class QuestionAnswerViewSetTestCase(APITestCase):

    def setUp(self):
        super().setUp()

        self.base_url = "/api/question-answer/"

        self.product = Product.objects.create()

    def test_create_question_answer_success(self):
        self.authenticate(self.user)

        data = {
            "product": self.product.pk,
            "content": "Test content"
        }

        res = self.client.post(
            self.base_url,
            data
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_201_CREATED
        )

        question_answer = QuestionAnswer.objects.last()
        self.assertTrue(question_answer)
        self.assertEqual(self.user, question_answer.user)
        self.assertEqual(data['product'], question_answer.product.pk)
        self.assertEqual(question_answer.reply, None)
        self.assertEqual(data['content'], question_answer.content)

    def test_create_question_answer_reply_success(self):
        self.authenticate(self.user)

        question_answer = QuestionAnswer.objects.create(
            user=self.user,
            product=self.product,
            content="Test content"
        )

        data = {
            "product": self.product.pk,
            "reply": question_answer.pk,
            "content": "Test content"
        }

        res = self.client.post(
            self.base_url,
            data
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_201_CREATED
        )

        question_answer = QuestionAnswer.objects.last()
        self.assertTrue(question_answer)
        self.assertEqual(self.user, question_answer.user)
        self.assertEqual(data['product'], question_answer.product.pk)
        self.assertEqual(data['reply'], question_answer.reply.pk)
        self.assertEqual(data['content'], question_answer.content)

    def test_update_question_answer_different_user_fail(self):
        self.authenticate(self.user2)

        question_answer_reply = QuestionAnswer.objects.create(
            user=self.user,
            product=self.product,
            content="Test content"
        )
        question_answer = QuestionAnswer.objects.create(
            user=self.user,
            product=self.product,
            content="Test content",
            reply=question_answer_reply
        )

        data = {
            "product": self.product.pk,
            "reply": question_answer_reply.pk,
            "content": "Test content"
        }

        url = f'{self.base_url}{question_answer.pk}/'

        res = self.client.put(
            url,
            data
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_update_question_answer_reply_success(self):
        self.authenticate(self.user)

        question_answer_reply = QuestionAnswer.objects.create(
            user=self.user,
            product=self.product,
            content="Test content"
        )
        question_answer = QuestionAnswer.objects.create(
            user=self.user,
            product=self.product,
            content="Test content",
            reply=question_answer_reply
        )

        data = {
            "product": self.product.pk,
            "reply": question_answer_reply.pk,
            "content": "Test content"
        }

        url = f'{self.base_url}{question_answer.pk}/'

        res = self.client.put(
            url,
            data
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_200_OK
        )

        question_answer.refresh_from_db()
        self.assertTrue(question_answer)
        self.assertEqual(data['product'], question_answer.product.pk)
        self.assertEqual(data['reply'], question_answer.reply.pk)
        self.assertEqual(data['content'], question_answer.content)

    def test_update_question_answer_success(self):
        self.authenticate(self.user)

        question_answer = QuestionAnswer.objects.create(
            user=self.user,
            product=self.product,
            content="Test content"
        )

        data = {
            "product": self.product.pk,
            "content": "Test content updated"
        }

        url = f'{self.base_url}{question_answer.pk}/'

        res = self.client.put(
            url,
            data
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_200_OK
        )

        question_answer.refresh_from_db()
        self.assertTrue(question_answer)
        self.assertEqual(data['product'], question_answer.product.pk)
        self.assertEqual(question_answer.reply, None)
        self.assertEqual(data['content'], question_answer.content)
