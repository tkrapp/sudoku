from lib.sudoku import Sudoku

def main():
    game = (
        '    54 6 '
        '167 2    '
        '  5  18 3'
        ' 8 4    9'
        '  16934  '
        '3    5 1 '
        '4 82  1  '
        '    8 594'
        ' 1 54    '
    )

    sudoku = Sudoku(game.replace(' ', '.'))

    print(sudoku)

    print(sudoku.get_row(4))

    print(sudoku.get_col(2))

    print(sudoku.get_block(4, 3))

    print(sudoku.possible(4, 3, 1))

    print(sudoku.candidates(4, 3))

if __name__ == '__main__':
    main()
