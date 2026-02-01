from dataclasses import dataclass

@dataclass
class WorkoutEntry:
    exercise_code: str
    normalized_exercise_code: str
    data: str