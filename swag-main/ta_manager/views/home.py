from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View


class Home(LoginRequiredMixin, View):
    def get(self, request):  # render initial home page
        return render(request, "home.html")  # landing page
