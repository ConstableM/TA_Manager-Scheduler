from django.test import TestCase, Client
from ta_manager.models import User


class RemoveUser_UnitTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User(username="hello")
        user.set_password("hello")
        user.save()
        self.loggedIn = self.client.login(username="hello", password="hello")
        self.list_user = []
        for i in range(10):
            temp_user = User(username=str(i))
            temp_user.save()
            self.list_user.append(temp_user)

    def test_remove_empty(self):
        selected_user = []
        response = self.client.post('/account/', {'user_select': selected_user,
                                                  "remove_user": "REMOVE"})
        message = response.context['message']
        self.assertEqual(message,"No user selected")

    def test_remove_valid_user(self):
        selected_user = []
        for i in range(3):
            selected_user.append(self.list_user[i])
        response = self.client.post('/account/', {'user_select': selected_user,
                                                  "remove_user": "REMOVE"})
        message = response.context['message']
        self.assertEqual(message, "Account(s) removed successful" )
        # New list is not equal to original list (10)
        self.assertEqual(len(response.context['userList']), 8)

    def test_remove_invalid_user(self):
        selected_user = []
        for i in range(4):
            user = User(username=str(10+i))
            selected_user.append(user)
        response = self.client.post('/account/', {'user_select': selected_user,
                                                  "remove_user": "REMOVE"})
        message = response.context['message']
        self.assertEqual(message, "Account removal failed, try again")
        # Original list stayed the same
        self.assertEqual(len(self.list_user),10)
