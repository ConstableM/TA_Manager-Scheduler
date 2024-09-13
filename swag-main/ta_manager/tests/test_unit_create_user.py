from django.test import TestCase, Client

from ta_manager.models import User


class CreateUser_UnitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(username="hello", first_name="hello", last_name="hello", email="hello@gmail.com",
                         phone="111-222-3333", address="10 Street")
        self.user.set_password("hello")
        self.user.save()
        self.loggedIn = self.client.login(username="hello", password="hello")

    def test_create_blank_username(self):
        response = self.client.post('/account/', {
            'password': 'something',
            "first_name": "Hello",
            "last_name": "hello",
            "email": "hello@uwm.edu",
            "phone_number": "111-222-3333",
            "address": "100000 Streets Look",
            "roles": "Admin",
            "create_user": "CREATE"})
        context = response.context
        self.assertEquals("Invalid Input", context['message'])

    def test_create_blank_password(self):
        response = self.client.post('/account/', {
            'username': 'something',
            "first_name": "Hello",
            "last_name": "hello",
            "email": "hello@uwm.edu",
            "phone_number": "111-222-3333",
            "address": "100000 Streets Look",
            "roles": "Admin",
            "create_user": "CREATE"})
        context = response.context
        self.assertEquals("Invalid Input", context['message'])

    def test_create_same_username(self):
        response = self.client.post('/account/', {
            'username': 'hello',
            'password': 'something',
            "first_name": "Hello",
            "last_name": "hello",
            "email": "hello@uwm.edu",
            "phone_number": "111-222-3333",
            "address": "100000 Streets Look",
            "roles": "Admin",
            "create_user": "CREATE"})
        context = response.context
        self.assertEquals("Account already exists", context['message'])
