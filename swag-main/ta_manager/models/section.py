from django.db import models
from ta_manager.models import User, Course


class Section(models.Model):
	DAY_CHOICES = [
		(1, 'Monday'),
		(2, 'Tuesday'),
		(3, 'Wednesday'),
		(4, 'Thursday'),
		(5, 'Friday'),
		(6, 'Saturday'),
		(7, 'Sunday')
	]
	id = models.IntegerField(unique=True, primary_key=True)
	section_name = models.CharField(max_length=150)
	ta = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	location = models.CharField(max_length=150, blank=False)  # ValidationError when a field is blank
	day_of_week = models.IntegerField(choices=DAY_CHOICES, default=1, blank=False)
	time = models.TimeField(blank=False)
	course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, null=False)

	class Meta:
		verbose_name = "section"
		verbose_name_plural = "sections"
		default_permissions = []
		permissions = [
			("view_all_section_data", "Can view all data of this section"),
			("create_section", "Can create new sections"),
			("view_ta_section_assignments", "Can view all sections that a TA is assigned to"),
			("assign_own_tas_to_section", "Can assign a TA assigned to the same course to a section of that course"),
			("assign_all_tas_to_section", "Can assign any TA to a section")
		]

	def __str__(self):
		return f"{self.course}: {self.section_name}"
