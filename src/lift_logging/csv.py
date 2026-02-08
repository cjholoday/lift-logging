import lift_logging.parsers
from lift_logging import models

class CSVPrinter:
    def print(self, workouts: list[models.Workout]) -> str:
        output_lines = []
        for workout in workouts:
            for entry in workout.entries:
                output_lines.append('{};{};{}\n'.format(workout.workout_date,
                                                        entry.normalized_exercise_code,
                                                        entry.data))
        return output_lines
