from ta_manager.models import User
from django.test import TestCase, Client


class Remove_User_Acceptance_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.account_list = []
        # Create 10 accounts
        for i in range(10):
            user = User(username=str(i), email=str(i) + '@gmail.com')
            user.set_password(str(i))
            user.save()
            self.account_list.append(user)

    def test_can_remove_user(self):
        # GIVEN the supervisor has logged into their account

        # When the user is not logged in and trying to enter the url /account/ they should be sent back with an error
        response = self.client.get('/account/', follow=True)
        self.assertRedirects(response, '/')
        self.assertEqual(response.context["error"], "User is not logged in")

        # When the user is logged in, they can now have permission to enter the url /account/
        logged_in = self.client.login(username="2", password=str(2))
        self.assertTrue(logged_in)

        # AND navigated to the accounts tab
        response = self.client.get('/account/')
        current_url = response.request.get('PATH_INFO')
        self.assertEqual(current_url, '/account/')

        # Simulating checkbox: (Deleting account number 3, 1, 7)
        deleting_account = [self.account_list[2], self.account_list[0], self.account_list[6]]
        # WHEN the supervisor selects the user’s profile
        # AND the supervisor clicks "REMOVE"
        response = self.client.post('/account/', {"user_select": deleting_account,
                                                  "remove_user": "REMOVE"})
        # THEN the user’s account is deleted
        newUserList = response.context['userList']
        # Compare the new list with the old list to see if the same User stay in the same position
        # (When deleted, it shouldn't)
        self.assertNotEquals(newUserList[0], self.account_list[0])
        self.assertNotEquals(newUserList[2], self.account_list[2])
        self.assertNotEquals(newUserList[6], self.account_list[6])
        # Original size is 10, new size is 7 since we are deleting 3 elements
        self.assertEqual(len(newUserList), 7)

    def test_unable_remove_not_select(self):
        # GIVEN the supervisor has logged into their account

        # When the user is not logged in and trying to enter the url /account/ they should be sent back with an error
        response = self.client.get('/account/', follow=True)
        self.assertRedirects(response, '/')
        self.assertEqual(response.context["error"], "User is not logged in")

        # When the user is logged in, they can now have permission to enter the url /account/
        logged_in = self.client.login(username="2", password=str(2))
        self.assertTrue(logged_in)

        # AND navigated to the accounts tab
        response = self.client.get('/account/')
        current_url = response.request.get('PATH_INFO')
        self.assertEqual(current_url, '/account/')

        # WHEN the supervisor does not select any user
        selected_user = []

        # AND the supervisor clicks "REMOVE"
        response = self.client.post('/account/', {"user_select": selected_user,
                                                  "remove_user": "REMOVE"})
        # THEN a message will show saying, "No user selected"
        self.assertEqual(response.context['message'], "No user selected")
        # There are still 10 users in the list.
        self.assertEqual(len(response.context['userList']),10)

    # Since we are using a selection of choices, this action can not be done.
    # But if someone is making a request through a program with the url, they will be able to make such request as
    # removing someone that is not in the data then it would return the message of "Account removal failed, try again"
    def test_unable_remove_invalid_user(self):
        # GIVEN the supervisor has logged into their account

        # When the user is not logged in and trying to enter the url /account/ they should be sent back with an error
        response = self.client.get('/account/', follow=True)
        self.assertRedirects(response, '/')
        self.assertEqual(response.context["error"], "User is not logged in")

        # When the user is logged in, they can now have permission to enter the url /account/
        logged_in = self.client.login(username="2", password=str(2))
        self.assertTrue(logged_in)

        # AND navigated to the accounts tab

        response = self.client.get('/account/')
        current_url = response.request.get('PATH_INFO')
        self.assertEqual(current_url, '/account/')

        # WHEN the supervisor select or enter a user that does not exist in the database
        unknown_user = User(username='newandunknown')
        selected_user = [unknown_user]
        # AND the supervisor clicks "REMOVE"
        response = self.client.post('/account/', {"user_select": selected_user,
                                                  "remove_user": "REMOVE"})
        # THEN a message will show saying, "Account removal failed, try again"
        self.assertEqual(response.context['message'], "Account removal failed, try again")
        # There are still 10 users in the list.
        self.assertEqual(len(response.context['userList']),10)




