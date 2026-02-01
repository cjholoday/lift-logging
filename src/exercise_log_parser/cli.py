import exercise_log_parser.parser

def main():
    parser = exercise_log_parser.parser.Parser()
    workouts = parser.parse([
        "1/28/26\n",
        "PUm...80#13,6,5\n",
        "... difficult\n",
        "HAc...5.5#11L,11R,8L,8R\n",
        "DLk...18#15,10\n",
        "... comment",
        "BRbt...35#17,11\n",
        "BCd...15#13,4\n",
        "... rushed\n",
    ])

    print(workouts)

if __name__ == "__main__":
    main()