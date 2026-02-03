import exercise_log_parser.workout
import exercise_log_parser.exercise_code_parser
import re

DATE_PREFIX_RE = re.compile(r"^\s*(\d{1,2}/\d{1,2}/\d{2,4})")

def extract_date_prefix(line: str) -> str | None:
    m = DATE_PREFIX_RE.match(line)
    if not m:
        return None
    return m.group(1)

class ParseError(Exception):
    """Base class for all parser errors."""
    def __init__(self, message: str, line: str | None = None, line_no: int | None = None):
        super().__init__(message)
        self.line_no = line_no
        self.line = line

    def __str__(self):
        loc = f" (line {self.line_no})" if self.line_no is not None else ""
        content = f"\n>> {self.line}" if self.line is not None else ""
        return f"{self.args[0]}{loc}{content}"

class Parser:
    def __init__(self):
        self._state_handlers = {
            'start': self.handle_state_start,
            'inworkout': self.handle_state_inworkout,
        }

    def parse(self, lines: list[str]) -> list[Workout]:
        state = 'start'
        workouts = []
        for idx, line in enumerate(lines):
            try:
                state = self._state_handlers[state](line, workouts)
            except ParseError as e:
                e.line_no = idx
                raise e

        return workouts
    
    def handle_state_start(self, line, workouts) -> str:
        if self.is_comment_or_empty(line):
            return 'start'
        
        date = extract_date_prefix(line)
        if date is not None:
            new_workout = exercise_log_parser.workout.Workout(date, [])
            workouts.append(new_workout)
            return 'inworkout'

        raise ParseError("Expected a date, comment, or whitespace", line, None)
        return 'start'

    def handle_state_inworkout(self, line, workouts) -> str:
        if not workouts:
            raise ParseError("No workouts but in state inworkout", line, None)

        curr_workout = workouts[-1]
        if self.is_comment_or_empty(line):
            return 'inworkout'

        date = extract_date_prefix(line)
        if date is not None:
            if not curr_workout.entries:
                raise ParseError("No workout entries for previous date", line, None)
            new_workout = exercise_log_parser.workout.Workout(date, [])
            workouts.append(new_workout)
            return 'inworkout'
        
        # We expect a workout entry since there isn't a comment, whitespace, or date line
        parts = line.strip().split('...', 1)
        if not parts:
            raise ParseError("This should be unreachable", line, None)
        if len(parts) < 2 or not parts[1]:
            raise ParseError("Expected sets and reps data to follow exercise code", line, None)
        
        exercise_code, set_and_reps_data = parts
        exercise_code = exercise_code.strip()
        set_and_reps_data = set_and_reps_data.strip()

        code_reader = exercise_log_parser.exercise_code_parser.ExerciseCodeParser()
        normalized_exercise_code = code_reader.normalize(exercise_code)

        curr_workout.entries.append(exercise_log_parser.workout_entry.WorkoutEntry(
            exercise_code,
            normalized_exercise_code,
            set_and_reps_data
        ))
        
        print(curr_workout.entries[-1])
        return 'inworkout'
    
    def is_comment_or_empty(self, line):
        if line.startswith('...'):
            # Ignore the line. It's a comment
            return True
        
        if line.strip() == "":
            # Only whitespace
            return True

        return False


