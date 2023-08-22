from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass(order=True)
class Student:
    """Returns a singleton by name."""
    name: str

    _instances = {}  # Dictionary to store instances by name.

    def __new__(cls, name):
        """Ensures returning a new instance by name."""
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
        return cls._instances[name]


@dataclass
class Presence:
    student: Student
    weekday: int
    from_hour: datetime.time
    to_hour: datetime.time
    class_id: str

    _MINUTE_TRESHOLD = 5

    def __new__(cls, *args):
        """Ensures only >= 5min attendance are instantiated."""
        if args:
            from_hour = cls._str_to_datetime(args[2])
            to_hour = cls._str_to_datetime(args[3])
            if to_hour - from_hour < timedelta(minutes=cls._MINUTE_TRESHOLD):
                return
        return super().__new__(cls)

    def __post_init__(self):
        # Validate student.
        if isinstance(self.student, str) or isinstance(self.student, Student):
            self.student = Student(self.student)
        else:
            raise ValueError("Student must be a string or a Student instance")
        # Validate from and to hours.
        if isinstance(self.from_hour, str):
            self.from_hour = self._str_to_datetime(self.from_hour)
        if isinstance(self.to_hour, str):
            self.to_hour = self._str_to_datetime(self.to_hour)
        # Validate weekday.
        self.validate_weekday()

    @classmethod
    def _str_to_datetime(cls, time_str: str) -> datetime:
        try:
            return datetime.strptime(time_str, '%H:%M')
        except Exception as error:
            raise ValueError(f"Error: {error}")

    def validate_weekday(self):
        if isinstance(self.weekday, str) and self.weekday.isdigit():
            self.weekday = int(self.weekday)
        if self.weekday < 1 or self.weekday > 7:
            raise ValueError("Weekday must be between 1 and 7")

    def get_minutes(self):
        return (self.to_hour - self.from_hour).seconds // 60


@dataclass(order=True)
class Report:
    minutes: Optional[int] = 0
    days: Optional[int] = 0
    student: Student = None

    _instances = {}  # Dictionary to store instances by student.
    _order = ('minutes', 'days')

    @classmethod
    def clean_instances(cls):
        cls._instances = {}

    def __new__(cls, *, student):
        """Ensures returning a new instance by student."""
        if student.name not in cls._instances:
            cls._instances[student.name] = {
                'class': super().__new__(cls),
                '_presences': [],
            }
        return cls._instances[student.name]['class']

    def add_presence(self, presence: Presence):
        self.presences.append(presence)
        self._instances[self.student.name]['_presences'] = self.presences

    @property
    def presences(self):
        return self._instances[self.student.name]['_presences']

    def compute_minutes_and_days(self):
        """Group presences by weekday and compute minutes and days."""
        minutes_by_weekday = {}
        minutes, days = 0, 0
        for presence in self.presences:
            if not minutes_by_weekday.get(presence.weekday):
                minutes_by_weekday[presence.weekday] = 0
                days += 1
            minutes_by_weekday[presence.weekday] += presence.get_minutes()
            minutes += minutes_by_weekday[presence.weekday]
        self.minutes, self.days = minutes, days

    def print_report(self):
        base = f"{self.student.name}: {self.minutes} minutes"
        if self.days:
            return f"{base} in {self.days} {'days' if self.days > 1 else 'day'}"
        return base
