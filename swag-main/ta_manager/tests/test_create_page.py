from django.contrib.auth.models import Group
from django.test import TestCase

from ta_manager.forms.create import CreateUserForm, CreateCourseForm, CreateSectionForm
from ta_manager.models import User


class TestCreatePage(TestCase):
	supervisor_user = None

	@classmethod
	def setUpTestData(cls):
		cls.supervisor_user = User.objects.create_user(username="sup", password="sup", uwm_id=1)
		cls.supervisor_user.groups.add(Group.objects.get(name="Supervisor"))

	def test_correct_perms(self):
		self.client.force_login(self.supervisor_user)
		resp = self.client.get("/create/", follow=True)
		self.assertEqual(resp.status_code, 200)

	def test_wrong_perms(self):
		other_user = User.objects.create_user(username="ta", password="ta", uwm_id=2)
		other_user.groups.add(Group.objects.get(name="TA"))

		self.client.force_login(other_user)
		resp = self.client.get("/create/", follow=True)
		self.assertEqual(resp.status_code, 403)

	def test_first_form_user(self):
		self.client.force_login(self.supervisor_user)
		resp = self.client.post("/create", {"subform": "User"})
		self.assertRedirects(resp, "/create/user/", status_code=301)
		self.assertEqual(resp.context.form, CreateUserForm)

	def test_first_form_course(self):
		self.client.force_login(self.supervisor_user)
		resp = self.client.post("/create", {"subform": "Course"})
		self.assertRedirects(resp, "/create/course/", status_code=301)
		self.assertEqual(resp.context.form, CreateCourseForm)

	def test_first_form_section(self):
		self.client.force_login(self.supervisor_user)
		resp = self.client.post("/create", {"subform": "Section"})
		self.assertRedirects(resp, "/create/section/", status_code=301)
		self.assertEqual(resp.context.form, CreateSectionForm)

	# TODO: test submitting first form,
	#  that each option gives you the right sub-form,
	#  and then validation logic for each sub-form
