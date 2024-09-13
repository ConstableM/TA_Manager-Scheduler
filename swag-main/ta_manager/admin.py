from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import forms

from .forms.create import CreateUserForm
from .models import User, Section, Course


class UpdateUserForm(forms.UserChangeForm):
	class Meta(forms.UserChangeForm.Meta):
		model = User


class MyUserAdmin(UserAdmin):
	form = UpdateUserForm
	fieldsets = (
		(None, {"fields": ("username", "password")}),
		("Personal info", {"fields": ("first_name", "last_name", "email", "uwm_id", "phone", "address")}),
		("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups")})
	)
	add_form = CreateUserForm
	add_fieldsets = (
		(None, {
			"classes": "wide",
			"fields": ("username", "password1", "password2", "uwm_id", "groups"),
		}),
	)
	filter_horizontal = []


admin.site.register(User, MyUserAdmin)
admin.site.register(Course)
admin.site.register(Section)
