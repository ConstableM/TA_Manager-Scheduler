from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.db import models
from phone_field import PhoneField


class SingleGroupUserManager(UserManager):
	def _create_user(self, username, email, password, **extra_fields):
		groups = extra_fields.pop("groups", None)
		if not groups or not Group.objects.filter(name=groups).exists():
			raise ValueError("Given group does not exist")
		elif not extra_fields.get("uwm_id", None):
			raise ValueError("UWM ID missing")
		return super()._create_user(username, email, password, groups=Group.objects.get(name=groups), **extra_fields)


class User(AbstractUser):
	uwm_id = models.IntegerField(verbose_name="UWM ID", unique=True, primary_key=True, help_text="Student/faculty ID")
	first_name = models.CharField(verbose_name="first name", max_length=150, blank=False)
	last_name = models.CharField(verbose_name="last name", max_length=150, blank=False)
	email = models.EmailField(verbose_name="email address", blank=False, unique=True)
	phone = PhoneField(verbose_name="contact phone number", help_text="Visible only to supervisors")
	address = models.TextField(verbose_name="mailing Address", max_length=120, help_text="Visible only to supervisors")
	# This name is a bit misleading since it's only a single group, but it's overriding what was a ManyToManyField
	groups = models.ForeignKey(Group, verbose_name="group", to_field="name", on_delete=models.CASCADE,
								related_name="user_set", related_query_name="user",
								help_text="The group this user belongs to.")

	objects = SingleGroupUserManager()  # necessary for user creation to work properly with a ForeignKey

	REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ["groups", "uwm_id"]  # used in createsuperuser only

	class Meta:
		verbose_name = "user"
		verbose_name_plural = "users"
		default_permissions = []
		permissions = [
			("view_all_user_data", "Can view all data of this user"),
			("edit_own_user_data", "Can edit their own info (not assignments)"),
			("edit_all_user_data", "Can edit info of all users"),
			("view_public_user_data", "Can view public info of all users (not phone or address)"),
			("create_user", "Can create new users"),
			("delete_user", "Can delete existing users"),
			("notify_own_tas", "Can notify TAs assigned to the same course as themselves"),
			("notify_all_users", "Can notify all users")
		]

	def assigned_courses(self):
		if str(self.groups) == "Instructor":
			return self.courses_instructing.all()
		elif str(self.groups) == "TA":
			return self.courses_taing.all()
		else:
			from ta_manager.models import Course
			return Course.objects.none()  # return a QuerySet of Courses no matter what

	def assigned_sections(self):  # template author should use `regroup` tag to group by course
		return self.section_set.all()
