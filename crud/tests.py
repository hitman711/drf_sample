""" List of test cases for Crud App
"""
import random
import json

from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from crud.models import (
    Question, Tenant
)

# Test user data
test_user = [
    {'username':'test_1', 'first_name':'test_1', 'last_name':'test_1', 'email':'test_1@test.com'},
    {'username':'test_2', 'first_name':'test_2', 'last_name':'test_2', 'email':'test_2@test.com'},
    {'username':'test_3', 'first_name':'test_3', 'last_name':'test_3', 'email':'test_3@test.com'},
]

# Test question data
test_question = [
    {
        'title':'What was the name of your elementary / primary school?',
        'private': random.choice([True, False]),
        'user':''
    },
    {
        'title':'In what city or town does your nearest sibling live?',
        'private': random.choice([True, False]),
        'user':''
    },
    {
        'title':'What time of the month when you born?',
        'private': random.choice([True, False]),
        'user':''
    }
]

# Create your tests here.
class QuestionAPIListViewTestCase(APITestCase):
    """ Test case class to check different scenario on question list API
    """
    question_list_url = reverse("question-list")

    def create_test_users(self):
        """ Create dummy test user record
        """
        for user_obj in test_user:
            User.objects.create(
                username=user_obj['username'],
                first_name=user_obj['first_name'],
                last_name=user_obj['last_name'],
                email=user_obj['email']
            ).set_password(
                User.objects.make_random_password()
            )

    def create_tenant(self):
        """ Create dummy tenant record
        """
        for user in User.objects.all():
            Tenant.objects.create(
                name=user.get_full_name()
            )

    def create_questions(self):
        """ Create dummy questions
        """
        user_list = User.objects.all()
        for question in test_question:
            Question.objects.create(
                title=question['title'],
                private=question['private'],
                user=random.choice(user_list)
            )

    def setUp(self):
        """ Set up dummy test data
        """
        self.create_test_users()
        self.create_tenant()
        self.create_questions()

    def test_tenant_key(self):
        """ Check API key following validation scenarios

        1. Check API response (200, 403)
        2. Check Valid API key
        3. Check API response
        """
        key = Tenant.objects.all().last()
        response = self.client.get(
            self.question_list_url, {'api_key':key.api_key}
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check blank API key
        response = self.client.get(
            self.question_list_url
        )
        # Check that the response is 403 OK.
        self.assertEqual(response.status_code, 403)

        # Check invalid API key
        response = self.client.get(
            self.question_list_url, {'api_key':'abc'}
        )
        # Check that the response is 403 OK.
        self.assertEqual(response.status_code, 403)

    def test_question_list(self):
        """ Check question list api response based on scenario

        1. Response always contain private false questions
        2. Check response status (200)
        3. Length of the response
        """
        correct_response = Question.objects.all()
        key = Tenant.objects.all().last()
        response = self.client.get(
            self.question_list_url, {'api_key':key.api_key}
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Convert byte response into str
        response_data = json.loads(response.content.decode('utf-8'))

        # Check valid condition
        self.assertTrue(len(response_data) == correct_response.exclude(private=True).count()
        )

        # Check invalid condition
        self.assertTrue(
            len(response_data) != correct_response.exclude(private=False).count()
        )

    def test_question_search(self):
        """ Check search scenarios on question list API

        1. Check different searches ('exact', 'contains', 'in', 'startswith',
        'icontains',) on title column of question model.
        2. Check response status (200)
        3. Length of the response
        """
        correct_response = Question.objects.filter(title__icontains='was the name')
        key = Tenant.objects.all().last()

        response = self.client.get(
            self.question_list_url, {
                'api_key': key.api_key,
                'title__icontains': 'was the name'
            }
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Convert byte response into str
        response_data = json.loads(response.content.decode('utf-8'))

        # Check valid condition
        self.assertTrue(len(response_data) == correct_response.exclude(private=True).count()
        )

        # Check invalid condition
        self.assertTrue(
            len(response_data) != correct_response.exclude(private=False).count()
        )

