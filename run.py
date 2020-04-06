from lib.sudoku import Sudoku


def main():
    game = (
        "6..98...."
        "13......."
        ".976..8.."
        # ---------
        ".5....2.."
        "8.62.57.9"
        "..2....8."
        # ---------
        "..3..162."
        "......397"
        "....34..8"
    )

    sudoku = Sudoku(game)

    print("Input")
    print(sudoku)

    solution_number = None
    for solution_number, solution in enumerate(sudoku.solve()):
        print(f"\nSolution number: {solution_number + 1:2d}")
        print(solution)

    if solution_number is None:
        print("There are no solutions")
    elif solution_number == 0:
        print("There is one solution")
    else:
        print(f"There are {solution_number + 1} solutions")


if __name__ == "__main__":
    main()
