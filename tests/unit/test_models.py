from hamcrest import assert_that, equal_to

from src.models import Student


class TestStudent:
    def test_singleton(self):
        student_1 = Student(name='Oscar')
        student_2 = Student(name='Oscar')
        student_3 = Student(name='Angel')
        assert_that(student_1, equal_to(student_2))
        assert_that(student_2, not equal_to(student_3))