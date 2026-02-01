import exercise_log_parser.workout_entry
from dataclasses import dataclass

@dataclass
class Workout:
    workout_date: date
    entries: list[WorkoutEntry]