from ta_manager.models import User
from django.test import TestCase, Client


class Create_User_Acceptance_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(username="hello", first_name="hello", last_name="hello", email="hello@gmail.com",
                         phone="111-222-3333", address="10 Street")
        self.user.set_password("hello")
        self.user.save()

    def test_can_create_user(self):
        # GIVEN the supervisor has logged into their account

        # When the user is not logged in and trying to enter the url /account/ they should be sent back with an error
        response = self.client.get('/account/', follow=True)
        self.assertRedirects(response, '/')
        self.assertEqual(response.context["error"], "User is not logged in")

        # When the user is logged in, they can now have permission to enter the url /account/
        logged_in = self.client.login(username="hello", password="hello")
        self.assertTrue(logged_in)

        # AND navigated to the accounts tab
        response = self.client.get('/account/')
        current_url = response.request.get('PATH_INFO')
        self.assertEqual(current_url, '/account/')

        # WHEN the supervisor has entered all information about new user
        # THEN the supervisor clicked on the create new account button
        response = self.client.post('/account/',
                                    {"username": "something",
                                     "password": "something",
                                     "first_name": "new",
                                     "last_name": "newlast",
                                     "email": "hello@uwm.edu",
                                     "address": "10 Streets",
                                     "phone_number": "111-222-3333",
                                     "roles": "Admin",
                                     'create_user': "CREATE"})

        # AND the form asks for what classes the instructor will be teaching (Sprint 2)
        # THEN the new account is added to the list of users
        context = response.context
        self.assertEqual("Account Created", context['message'])
        # Checking the user list after with an expected list.
        expectedUserList = ["hello", "something"]
        i = 0
        for user in context['userList']:
            self.assertEqual(user.username, expectedUserList[i])
            i += 1

    def test_can_create_already_exists(self):
        # GIVEN the supervisor has logged into their account
        # AND the account they want to create already exists

        # When the user is not logged in and trying to enter the url /account/ they should be sent back with an error
        response = self.client.get('/account/', follow=True)
        self.assertRedirects(response, '/')
        self.assertEqual(response.context["error"], "User is not logged in")

        # When the user is logged in, they can now have permission to enter the url /account/
        logged_in = self.client.login(username="hello", password="hello")
        self.assertTrue(logged_in)

        # AND navigated to the accounts tab
        response = self.client.get('/account/')
        current_url = response.request.get('PATH_INFO')
        self.assertEqual(current_url, '/account/')

        # WHEN the supervisor filled out the form information for new user
        # AND the filled out information for new user is already exists in the database
        response = self.client.post('/account/',
                                    {"username": "hello",
                                     "password": "hello",
                                     "first_name": "new",
                                     "last_name": "newlast",
                                     "email": "hello@uwm.edu",
                                     "address": "10 Streets",
                                     "phone_number": "111-222-3333",
                                     "roles": "Admin",
                                     'create_user': "CREATE"})
        # THEN the supervisor clicked "Create" button, a message is shown saying, "Account already exists"
        context = response.context
        self.assertEqual("Account already exists", context['message'])

        # WHEN the supervisor check the list of user
        # THEN the list of user is shown WITHOUT duplication.
        expectedUserList = ['hello']
        actualUserList = context['userList']
        self.assertEqual(len(actualUserList), 1)
        self.assertEquals(actualUserList[0].username, expectedUserList[0])
