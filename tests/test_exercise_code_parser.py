from lift_logging.parsers import ExerciseCodeParser
from lift_logging.parsers import ParseError
from lift_logging.models import Workout
from lift_logging.models import WorkoutEntry
import pytest

def test_unpack_positive():
    parser = ExerciseCodeParser()

    uppers, lowers, symbols = parser.unpack("CPm")
    assert uppers == 'CP'
    assert lowers == 'm'
    assert symbols == ''

    uppers, lowers, symbols = parser.unpack("PUm")
    assert uppers == 'PU'
    assert lowers == 'm'
    assert symbols == ''

    uppers, lowers, symbols = parser.unpack("CFc")
    assert uppers == 'CF'
    assert lowers == 'c'
    assert symbols == ''

    uppers, lowers, symbols = parser.unpack("TEc^")
    assert uppers == 'TE'
    assert lowers == 'c'
    assert symbols == '^'

    uppers, lowers, symbols = parser.unpack("SPsd")
    assert uppers == 'SP'
    assert lowers == 'sd'
    assert symbols == ''

def test_unpack_missing_category():
    parser = ExerciseCodeParser()

    # Missing exercise
    with pytest.raises(ParseError):
        parser.unpack("m")

    # Missing variation
    with pytest.raises(ParseError):
        parser.unpack("PU")
    
    # Missing symbol variation (should not throw as it's optional)
    parser.unpack("CPm")


def test_unpack_category_order():
    parser = ExerciseCodeParser()

    # Wrong order
    with pytest.raises(ParseError):
        parser.unpack("mPU")

    # Variations begin and end
    with pytest.raises(ParseError):
        parser.unpack("mPUm")
    
    # Two exercises
    with pytest.raises(ParseError):
        parser.unpack("PUmCFc")

    # Symbol variation coming first
    with pytest.raises(ParseError):
        parser.unpack("^TEc")

    # Symbol variation coming second
    with pytest.raises(ParseError):
        parser.unpack("TE^c")

def test_normalize_positive():
    parser = ExerciseCodeParser()

    code = parser.normalize("SPsd")
    assert code == 'SPds'

    code = parser.normalize("SPds")
    assert code == 'SPds'

    code = parser.normalize("TEd_>")
    assert code == 'TEd>_'
