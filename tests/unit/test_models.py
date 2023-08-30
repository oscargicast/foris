from hamcrest import assert_that, equal_to
from src.models import Student, Presence, ShortPresenceError


class TestStudent:
    def test_model(self):
        student_1 = Student(name='Oscar')
        student_2 = Student(name='Oscar')
        student_3 = Student(name='Angel')
        assert_that(student_1, equal_to(student_2))
        assert_that(student_2, not equal_to(student_3))

class TestPresence:
    def test_model(self):
        # Student 1.
        student_1 = Student(name='Oscar')
        student_1.register_presence(Presence(
            weekday="1",
            from_hour="08:10",
            to_hour="09:10",
            class_id="1",
        ))
        assert_that(student_1.minutes, equal_to(60))
        assert_that(student_1.days, equal_to(1))

        student_1.register_presence(Presence(
            weekday="2",
            from_hour="18:00",
            to_hour="19:00",
            class_id="1",
        ))
        assert_that(student_1.minutes, equal_to(60*2))
        assert_that(student_1.days, equal_to(2))

        try:
            student_1.register_presence(Presence(
                weekday="3",
                from_hour="18:00",
                to_hour="18:04",
                class_id="1",
            ))
        except ShortPresenceError:
            pass
        assert_that(student_1.minutes, equal_to(60*2))
        assert_that(student_1.days, equal_to(2))

        # Student_2 .
        student_2 = Student(name='Angel')
        student_2.register_presence(Presence(
            weekday="1",
            from_hour="08:10",
            to_hour="09:10",
            class_id="1",
        ))

        # Checks order.
        assert_that(student_1.minutes, equal_to(60*2))
        assert_that(student_2.minutes, equal_to(60*1))
        assert_that(student_1 > student_2, equal_to(True))

        #Changing the order.
        student_2.register_presence(Presence(
            weekday="2",
            from_hour="08:10",
            to_hour="18:10",
            class_id="1",
        ))
        assert_that(student_1.minutes, equal_to(60*2))
        assert_that(student_2.minutes, equal_to(60*11))
        assert_that(student_1 < student_2, equal_to(True))