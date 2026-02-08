from .workout_entry import WorkoutEntry
from dataclasses import dataclass

@dataclass
class Workout:
    workout_date: date
    entries: list[WorkoutEntry]