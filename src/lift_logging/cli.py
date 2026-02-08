import lift_logging.parsers
import lift_logging.csv


import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m lift_logging.cli LOGFILE")
        sys.exit(1)

    exercise_log_path = sys.argv[1]

    with open(exercise_log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    parser = lift_logging.parsers.ExerciseLogParser()
    workouts = parser.parse(lines)

    printer = lift_logging.csv.CSVPrinter()
    output = printer.print(workouts)
    for line in output:
        print(line.rstrip())

if __name__ == "__main__":
    main()