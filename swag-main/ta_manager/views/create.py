from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from ta_manager.forms.create import CreateWhatForm, CreateUserForm, CreateCourseForm, CreateSectionForm

required_permissions = ["create_user", "create_course", "create_section"]


class CreateWhat(LoginRequiredMixin, PermissionRequiredMixin, View):
	permission_required = required_permissions
	raise_exception = True

	def get(self, request):
		return render(request, "create.html", {"form": CreateWhatForm(), "message": None})

	def post(self, request):
		form = CreateWhatForm(request.POST)
		if form.is_valid():
			return redirect(f"/create/{form.cleaned_data['subform']}/")
		else:
			return render(request, "create.html", {"form": form, "message": form.errors})


class CreateUser(LoginRequiredMixin, PermissionRequiredMixin, View):
	permission_required = required_permissions[0]
	raise_exception = True

	def get(self, request):
		return render(request, "create.html", {"form": CreateUserForm(), "message": None})

	def post(self, request):
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("/create/")
		else:
			return render(request, "create.html", {"form": form, "message": form.errors})


class CreateCourse(LoginRequiredMixin, PermissionRequiredMixin, View):
	permission_required = required_permissions[1]
	raise_exception = True

	def get(self, request):
		return render(request, "create.html", {"form": CreateCourseForm(), "message": None})

	def post(self, request):
		form = CreateCourseForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("/create/")
		else:
			return render(request, "create.html", {"form": form, "message": form.errors})


class CreateSection(LoginRequiredMixin, PermissionRequiredMixin, View):
	permission_required = required_permissions[2]
	raise_exception = True

	def get(self, request):
		return render(request, "create.html", {"form": CreateSectionForm(), "message": None})

	def post(self, request):
		form = CreateSectionForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("/create/")
		else:
			return render(request, "create.html", {"form": form, "message": form.errors})
