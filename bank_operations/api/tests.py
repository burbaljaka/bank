from django.test import TestCase, override_settings
from .models import Client
from .tasks import process_operation
from django.urls import reverse
import json
from rest_framework import status
from celery.contrib.testing.worker import start_worker
from django.test import TransactionTestCase
from bank_operations.celery import app

# Create your tests here.

class APITests(TestCase):
    @classmethod
    def setUpClass(cls):
        # super().setUpClass()
        # cls.celery_worker = start_worker(app)
        # cls.celery_worker.__enter__()

        cls.user_1_good_balance = Client.objects.create(id='26c940a1-7228-4ea2-a3bce6460b172040',
                                                      name='Петров Иван Сергеевич',
                                                      balance=1700,
                                                      hold=200,
                                                      status=True)
        cls.user_2_closed_account = Client.objects.create(id='867f0924-a917-4711-939b90b179a96392',
                                                          name='Петечкин Петр Измаилович',
                                                          balance=1000000,
                                                          hold=1,
                                                          status=False)

        cls.user_3_equal_balanse_and_hold = Client.objects.create(id='7badc8f8-65bc-449a-8cde855234ac63e1',
                                                                  name='Kazitsky Jason',
                                                                  balance=200,
                                                                  hold=200,
                                                                  status=True)

        cls.user_4_equal_low_balanse = Client.objects.create(id='5597cc3d-c948-48a0-b711-393edf20d9c0',
                                                            name='Пархоменко Антон Александрович',
                                                            balance=10,
                                                            hold=300,
                                                            status=True)


    def test_addition_endpoint(self):
        amount = 100
        response_1 = self.client.post(reverse('addition'),
                                      json.dumps({'amount': amount, 'id': self.user_1_good_balance.id}),
                                      content_type='application/json')

        response_2 = self.client.post(reverse('addition'),
                                      json.dumps({'amount': amount, 'id': self.user_2_closed_account.id}),
                                      content_type='application/json')

        response_3 = self.client.post(reverse('addition'),
                                      json.dumps({'amount': amount, 'id': self.user_3_equal_balanse_and_hold.id}),
                                      content_type='application/json')

        response_4 = self.client.post(reverse('addition'),
                                      json.dumps({'amount': amount, 'id': self.user_4_equal_low_balanse.id}),
                                      content_type='application/json')


        #checking status codes
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_200_OK)
        self.assertEqual(response_4.status_code, status.HTTP_200_OK)

    def test_substraction_endpoint(self):
        amount = 100
        response_1 = self.client.post(reverse('substraction'),
                                      json.dumps({'amount': amount, 'id': self.user_1_good_balance.id}),
                                      content_type='application/json')

        response_2 = self.client.post(reverse('substraction'),
                                      json.dumps({'amount': amount, 'id': self.user_2_closed_account.id}),
                                      content_type='application/json')

        response_3 = self.client.post(reverse('substraction'),
                                      json.dumps({'amount': amount, 'id': self.user_3_equal_balanse_and_hold.id}),
                                      content_type='application/json')

        response_4 = self.client.post(reverse('substraction'),
                                      json.dumps({'amount': amount, 'id': self.user_4_equal_low_balanse.id}),
                                      content_type='application/json')


        # checking status codes
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_4.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ping_endpoint(self):
        response = self.client.get(reverse('test'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Service is up currently')

    def test_get_status_endpoint(self):
        response = self.client.post(reverse('get_status'), json.dumps({'id': self.user_1_good_balance.id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Client account info')
        self.assertEqual(response.data['addition']['name'], self.user_1_good_balance.name)


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPOGATES=True)
    def test_celery_task_addition(self):
        result = process_operation(100, self.user_1_good_balance.id, 'addition')
        self.assertEqual(self.user_1_good_balance.balance, 1800)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None, None, None)
