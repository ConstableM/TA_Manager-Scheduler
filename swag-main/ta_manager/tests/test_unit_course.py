from datetime import datetime

from django.test import TestCase

from ta_manager.models import User, Course, Section


class MyTestCase(TestCase):
	supervisor, instructor1, instructor2, ta1, ta2 = None, None, None, None, None
	course1, course2, course3 = None, None, None
	section1, section2, section3 = None, None, None

	@classmethod
	def setUpTestData(cls):
		cls.supervisor = User.objects.create_user(username="supervisor", uwm_id=1, groups="Supervisor")
		cls.instructor1 = User.objects.create_user(username="instructor1", uwm_id=2, groups="Instructor")
		cls.instructor2 = User.objects.create_user(username="instructor2", uwm_id=3, groups="Instructor")
		cls.ta1 = User.objects.create_user(username="ta1", uwm_id=4, groups="TA")
		cls.ta2 = User.objects.create_user(username="ta2", uwm_id=5, groups="TA")

		cls.course1 = Course.objects.create(id=1, name="course1", department="department1",
											term="term1", instructor=cls.instructor1)
		cls.course1.tas.set([cls.ta1])
		cls.course2 = Course.objects.create(id=2, name="course2", department="department2",
											term="term2", instructor=cls.instructor1)
		cls.course2.tas.set([cls.ta1])
		cls.course3 = Course.objects.create(id=3, name="course3", department="department3",
											term="term3", instructor=cls.instructor2)

		cls.section1 = Section.objects.create(id=1, section_name="section1", course=cls.course1,
												time=datetime.now(), ta=cls.ta1)
		cls.section2 = Section.objects.create(id=2, section_name="section2", course=cls.course1,
												time=datetime.now(), ta=cls.ta1)
		cls.section3 = Section.objects.create(id=3, section_name="section3", course=cls.course2, time=datetime.now())

	def test_sections(self):
		self.assertEqual(list(self.course1.sections()), [self.section1, self.section2])
		self.assertEqual(list(self.course2.sections()), [self.section3])
		self.assertEqual(list(self.course3.sections()), [])
