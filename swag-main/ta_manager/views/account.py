from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View

from ta_manager.models import User


class Account(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'account.html', {"userList": self.List_Account})
        # Check for permission in Sprint 2

    def post(self, request):
        # Check if the post is Creating an Account or Listing the users
        # Create an Account
        message = None
        if 'create_user' in request.POST:
            try:
                user_name = request.POST['username']
                user_password = request.POST['password']
                first = request.POST['first_name']
                last = request.POST['last_name']
                email = request.POST['email']
                address = request.POST['address']
                phone = request.POST['phone_number']
                role = request.POST['roles']
                if self.Create_Account(user_name=user_name,
                                       user_password=user_password,
                                       first_name=first,
                                       last_name=last,
                                       user_email=email,
                                       address=address,
                                       phone_number=phone,
                                       role=role) is False:
                    message = "Account already exists"
                else:
                    message = "Account Created"
            except KeyError:
                return render(request, 'account.html', {'message': 'Invalid Input'})
        elif 'remove_user' in request.POST:
            selected_users = request.POST.getlist('user_select')
            if len(selected_users) == 0:
                message = "No user selected"
            elif not self.Remove_Account(selected_users):
                message = "Account removal failed, try again"
            else:
                message = "Account(s) removed successful"
        # List all the accounts
        return render(request, 'account.html', {"message": message, "userList": self.List_Account()})

    def Create_Account(self, user_name, user_password, first_name, last_name, user_email, phone_number, address, role):
        if User.objects.filter(username=user_name).exists():
            return False
        try:
            user = User(username=user_name, first_name=first_name, last_name=last_name, email=user_email,
                        phone=phone_number, address=address)
            user.set_password(user_password)
            user.save()
            return True
        except IntegrityError:
            return False

    def List_Account(self):
        return User.objects.all()

    def Remove_Account(self, userList):
        for user in userList:
            try:
                user = User.objects.get(username=user)
                user.delete()
            except User.DoesNotExist:
                return False
        return True
