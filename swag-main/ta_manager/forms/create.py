from django import forms
from django.contrib.auth import forms as auth_forms

from ta_manager import models


class CreateWhatForm(forms.Form):
	title = "Create"
	subform_choices = (
		("user", "User"),
		("course", "Course"),
		("section", "Section")
	)
	subform = forms.ChoiceField(choices=subform_choices, label="What do you want to create?", label_suffix="")


class CreateUserForm(auth_forms.UserCreationForm):
	title = "Create User"

	class Meta(auth_forms.UserCreationForm.Meta):
		model = models.User
		fields = auth_forms.UserCreationForm.Meta.fields + ("uwm_id", "groups", "phone", "address", "email")


class CreateCourseForm(forms.ModelForm):
	title = "Create Course"

	class Meta:
		model = models.Course
		fields = "__all__"


class CreateSectionForm(forms.ModelForm):
	title = "Create Section"

	class Meta:
		model = models.Section
		fields = "__all__"
