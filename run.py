from lib.sudoku import Sudoku


def main():
    game = (
        "....54.6."
        "167.2...."
        "..5..18.3"
        # ---------
        ".8.4....9"
        "..16934.."
        "3....5.1."
        # ---------
        "4.82..1.."
        "....8.594"
        ".1.54...."
    )

    # game = (
    #     '1       2'
    #     '         '
    #     '         '
    #     '         '
    #     '         '
    #     '         '
    #     '         '
    #     '         '
    #     '2       1'
    # )

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
