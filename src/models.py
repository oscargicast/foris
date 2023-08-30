from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass()
class Student:
    name: str
    presences: list[Presence] = field(default_factory=list, init=False, repr=False)
    minutes: int = field(default=0, init=False)
    days: int = field(default=0, init=False)
    weekdays: set[int | str] = field(default_factory=set, init=False, repr=False)

    def __lt__(self, other: Student) -> bool:
        return self.minutes < other.minutes

    def register_presence(self, presence: Presence | None):
        if not presence:
            return
        self.presences.append(presence)
        self.minutes += presence.minutes_elapsed
        self.weekdays.add(presence.weekday)
        self.days = len(self.weekdays)

    def print_report(self):
        base = f"{self.name}: {self.minutes} minutes"
        if self.days:
            return f"{base} in {self.days} {'days' if self.days > 1 else 'day'}"
        return base


class ShortPresenceError(Exception):

    MESSAGE = "The attendance is too short to be considered"

    def __init__(self, message: str = ""):
        if not message:
            message = self.MESSAGE
        super().__init__(message)


@dataclass()
class Presence:
    weekday: int | str
    from_hour: datetime | str
    to_hour: datetime | str
    class_id: str

    _MINUTE_TRESHOLD = 5  # In minutes.

    def __post_init__(self):
        # Validate from and to hours.
        self.from_hour = self.validate_hour(self.from_hour)
        self.to_hour = self.validate_hour(self.to_hour)
        # Ensures only >= 5min attendance are instantiated.
        time_diff = self.to_hour - self.from_hour
        if time_diff < timedelta(minutes=self._MINUTE_TRESHOLD):
            raise ShortPresenceError()
        # Validate weekday.
        self.validate_weekday()

    @classmethod
    def _str_to_datetime(cls, time_str: str) -> datetime:
        try:
            return datetime.strptime(time_str, '%H:%M')
        except Exception as error:
            raise ValueError(f"Error: {error}")

    def validate_hour(self, hour: str | datetime) -> datetime:
        if isinstance(hour, str):
            hour = self._str_to_datetime(hour)
        else:
            raise ValueError(
                "from and to hours must have a str HH:MM format "
                "or datetime.time"
            )
        return hour

    def validate_weekday(self):
        if isinstance(self.weekday, str) and self.weekday.isdigit():
            self.weekday = int(self.weekday)
        else:
            raise ValueError("weekday must be an integer")
        if self.weekday < 1 or self.weekday > 7:
            raise ValueError("weekday must be between 1 and 7")

    @property
    def minutes_elapsed(self) -> int:
        return (self.to_hour - self.from_hour).seconds // 60