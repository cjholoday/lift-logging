

from lift_logging.parsers import ExerciseLogParser
from lift_logging.parsers import ParseError
from lift_logging.models.workout import Workout
from lift_logging.models.workout_entry import WorkoutEntry
import pytest

def test_basic():
    parser = ExerciseLogParser()
    actual_workouts = parser.parse([
        "1/28/26\n",
        "PUm...80#13,6,5...80#2\n",
        "... difficult\n",
        "HAc...5.5#11L,11R,8L,8R\n",
        "DLk...18#15,10\n",
        "... comment",
        "BRbt...35#17,11\n",
        "BCd...15#13,4\n",
        "... rushed\n",
    ])

    assert len(actual_workouts) == 1
    assert len(actual_workouts[0].entries) == 5
    
    expected_workouts = [
        Workout('1/28/26', [
            WorkoutEntry('PUm', 'PUm', '80#13,6,5...80#2'),
            WorkoutEntry('HAc', 'HAc', '5.5#11L,11R,8L,8R'),
            WorkoutEntry('DLk', 'DLk', '18#15,10'),
            WorkoutEntry('BRbt', 'BRbt', '35#17,11'),
            WorkoutEntry('BCd', 'BCd', '15#13,4'),
        ])
    ]
    assert actual_workouts == expected_workouts

def test_two_workouts():
    parser = ExerciseLogParser()
    actual_workouts = parser.parse([
        "1/28/26\n",
        "PUm...80#13,6,5...80#2\n",
        "HAc...5.5#11L,11R,8L,8R\n",
        "1/31/26\n",    
        "CPm...40#17,14,13,12\n",
    ])

    assert len(actual_workouts) == 2
    assert len(actual_workouts[0].entries) == 2
    assert len(actual_workouts[1].entries) == 1

    expected_workouts = [
        Workout('1/28/26', [
            WorkoutEntry('PUm', 'PUm', '80#13,6,5...80#2'),
            WorkoutEntry('HAc', 'HAc', '5.5#11L,11R,8L,8R')
        ]),
        Workout('1/31/26', [
            WorkoutEntry('CPm', 'CPm', '40#17,14,13,12'),
        ]),
    ]
    
    assert actual_workouts == expected_workouts

def test_whitespace_okay():
    parser = ExerciseLogParser()
    actual_workouts = parser.parse([
        "   ",
        "1/28/26\n",
        "",
        "  ",
        "    PUm... 80#13,6,5...80#2\n",
        " HAc ...5.5#11L,11R,8L,8R \n",
        "",
        " 1/31/26 \n",    
        "",
        "CPm...40#17, 14,1 3,12\n",
        "",
    ])

    assert len(actual_workouts) == 2
    assert len(actual_workouts[0].entries) == 2
    assert len(actual_workouts[1].entries) == 1

    expected_workouts = [
        Workout('1/28/26', [
            WorkoutEntry('PUm', 'PUm', '80#13,6,5...80#2'),
            WorkoutEntry('HAc', 'HAc', '5.5#11L,11R,8L,8R')
        ]),
        Workout('1/31/26', [
            WorkoutEntry('CPm', 'CPm', '40#17, 14,1 3,12'),
        ]),
    ]
    
    assert actual_workouts == expected_workouts


def test_whitespace_okay():
    parser = ExerciseLogParser()
    actual_workouts = parser.parse([
        "   ",
        "1/28/26\n",
        "",
        "  ",
        "    PUm... 80#13,6,5...80#2\n",
        " HAc ...5.5#11L,11R,8L,8R \n",
        "",
        " 1/31/26 \n",    
        "",
        "CPm...40#17, 14,1 3,12",
        "",
    ])

    assert len(actual_workouts) == 2
    assert len(actual_workouts[0].entries) == 2
    assert len(actual_workouts[1].entries) == 1

    expected_workouts = [
        Workout('1/28/26', [
            WorkoutEntry('PUm', 'PUm', '80#13,6,5...80#2'),
            WorkoutEntry('HAc', 'HAc', '5.5#11L,11R,8L,8R')
        ]),
        Workout('1/31/26', [
            WorkoutEntry('CPm', 'CPm', '40#17, 14,1 3,12'),
        ]),
    ]
    
    assert actual_workouts == expected_workouts

def test_negative_no_workout_data():
    parser = ExerciseLogParser()

    with pytest.raises(ParseError):
        parser.parse([
            "1/28/26\n",
            "1/31/26\n",
        ])

def test_negative_data_precedes_date():
    parser = ExerciseLogParser()

    with pytest.raises(ParseError):
        parser.parse([
            "PUm...80#13,6,5...80#2\n",
            "1/28/26\n",
        ])

def test_negative_data_precedes_date():
    parser = ExerciseLogParser()

    with pytest.raises(ParseError):
        parser.parse([
            "PUm...80#13,6,5...80#2\n",
            "1/28/26\n",
        ])

def test_negative_invalid_date():
    parser = ExerciseLogParser()

    with pytest.raises(ParseError):
        parser.parse([
            "1/31\n",
        ])

def test_negative_missing_data():
    parser = ExerciseLogParser()

    with pytest.raises(ParseError):
        parser.parse([
            "1/28/26\n",
            "PUm\n",
        ])
    
    with pytest.raises(ParseError):
        parser.parse([
            "1/28/26\n",
            "PUm...\n",
        ])