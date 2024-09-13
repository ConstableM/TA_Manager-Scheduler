from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from ta_manager.models import Course


class CourseView(LoginRequiredMixin, View):
    def get(self, request):
        error = request.session.get('error', '')
        courses = list(Course.objects.all())
        return render(request, "course.html", {"courses": courses, "error": error})

    def post(self, request):
            return redirect('/account/')  # replace this with login la
