from django.test import TestCase, Client

from ta_manager.models import Course, User


class Test_List_Course(TestCase):

    def setUp(self):
        self.client = Client()
        self.course_list = []
        self.user = User(username="hello", first_name="hello", last_name="hello", email="hello@uwm.edu",
                         phone="111-222-3333", address="10 Street", uwm_id="123333")
        self.user.set_password("hello")
        self.user.save()
        for i in range(10):
            course = Course(name=str(i))
            course.save()
            self.course_list.append(course)

    def test_lists_all_courses(self):
        self.client.login(username="hello", password="hello")
        respond = self.client.get("/course/")
        count = 0
        for i in respond.context["courses"]:
           self.assertEqual(i, self.course_list[count])
           count +=1