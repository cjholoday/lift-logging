
class ExerciseCodeParser:
    def normalize(self, exercise_code: str) -> str:
        # throws if invalid
        exercise_code = exercise_code.strip()
        self.validate(exercise_code)
        return exercise_code # CHTODO


    def validate(self, exercise_code: str):
        pass # CHTODO