import lift_logging.workout_entry
from dataclasses import dataclass

@dataclass
class Workout:
    workout_date: date
    entries: list[WorkoutEntry]