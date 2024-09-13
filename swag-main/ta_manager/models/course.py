from django.core.exceptions import ValidationError
from django.db import models

from ta_manager.models import User


class Course(models.Model):
	id = models.IntegerField(verbose_name="Course ID", unique=True, primary_key=True)
	name = models.CharField(verbose_name="Course Name", max_length=120)
	department = models.CharField(verbose_name="Department", max_length=120)
	term = models.CharField(verbose_name="Course Term", max_length=120)

	instructor = models.ForeignKey(User, verbose_name="Instructor", on_delete=models.CASCADE,
									related_name="courses_instructing")
	tas = models.ManyToManyField(User, verbose_name="TAs", related_name="courses_taing",
									help_text="TAs assigned to this course can be assigned to sections of this course"
												"by instructors.")

	class Meta:
		verbose_name = "course"
		verbose_name_plural = "courses"
		default_permissions = []
		permissions = [
			("view_all_course_data", "Can view all data of this course"),
			("create_course", "Can create new courses"),
			("view_own_course_assignments", "Can view courses they are assigned to"),
			("assign_all_instructors", "Can assign any instructor to a course"),
			("assign_all_tas_to_course", "Can assign any TA to a course")
		]

	def clean(self):
		if self.instructor.groups.name != "Instructor":
			raise ValidationError(f"Instructor must be a user with Instructor group")
		for ta in self.tas.all():
			if ta.groups.name != "TA":
				raise ValidationError(f"User {ta.user.username} does not have TA group")

	def sections(self):
		return self.section_set.all()

	def __str__(self):
		return self.name
