from lift_logging import models
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
        loc = f"Error occured on line {self.line_no}" if self.line_no is not None else ""
        content = f"Line Content:\n{self.line}" if self.line is not None else ""
        return f"{self.args[0]}\n{loc}\n{content}"


class ExerciseCodeParser:
    def normalize(self, exercise_code: str) -> str:
        uppers, lowers, symbols = self.unpack(exercise_code)
        lowers = "".join(sorted(lowers))
        symbols = "".join(sorted(symbols))
        return uppers + lowers + symbols

    def unpack(self, exercise_code: str) -> tuple[str, str, str]:
        EXERCISE_CODE_RE = re.compile(
    r"^(?P<upper>[A-Z]+)(?P<lower>[a-z]+)(?P<symbols>[^A-Za-z0-9]*)$")
        m = EXERCISE_CODE_RE.fullmatch(exercise_code)
        if not m:
            raise ParseError(
                "Exercise code '{}' does not match expected format. Expected format: EEEvvv$$$ where EEE is the exercise being done in uppercase, vvv is the variation done in lowercase, and $$$ are optional symbols further distinguishing variation".format(exercise_code), None, None)
        return m.group("upper"), m.group("lower"), m.group("symbols")

class ExerciseLogParser:
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
            new_workout = models.Workout(date, [])
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
            new_workout = models.Workout(date, [])
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

        try:
            code_parser = ExerciseCodeParser()
            normalized_exercise_code = code_parser.normalize(exercise_code)
        except ParseError as e:
            e.line = line
            raise e

        curr_workout.entries.append(models.WorkoutEntry(
            exercise_code,
            normalized_exercise_code,
            set_and_reps_data
        ))
        
        return 'inworkout'
    
    def is_comment_or_empty(self, line):
        if line.lstrip().startswith('...'):
            # Ignore the line. It's a comment
            return True
        
        if line.strip() == "":
            # Only whitespace
            return True

        return False

