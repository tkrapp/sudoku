"""
This module contains a class which can solve Sudoku games
via backtracking.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from itertools import product, tee
from typing import ClassVar, Iterable, List


@dataclass
class Sudoku:
    "A class representing a (not) completed sudoku game"

    game: str

    ALL_NUMS: ClassVar = set("123456789")
    FIELD_SIZE: ClassVar = 9
    SQUARE_SIZE: Classvar = 3

    def __str__(self) -> str:
        "Pretty print the field"

        sep = "+-----+-----+-----+"
        rows = [
            "|"
            + "|".join(
                " ".join(row[idx : idx + self.SQUARE_SIZE])
                for idx in range(0, self.FIELD_SIZE, self.SQUARE_SIZE)
            )
            + "|"
            for row in self.iter_rows()
        ]

        return "\n".join([sep, *rows[0:3], sep, *rows[3:6], sep, *rows[6:9], sep,])

    def get_row(self, y: int) -> str:
        "Get a specific row of the field"

        return self.game[self.FIELD_SIZE * y : (self.FIELD_SIZE * y) + self.FIELD_SIZE]

    def get_col(self, x: int) -> str:
        "Get a specific column of the field"

        return "".join(
            self.game[position]
            for position in range(x, len(self.game), self.FIELD_SIZE)
        )

    def get_square(self, x: int, y: int) -> str:
        """
        Get a specific square (3x3-block) of the field.
        x and y may be located anywhere inside the square
        and don't need to be the correct start coordinates
        of it.
        """

        square_x = x // self.SQUARE_SIZE
        square_y = y // self.SQUARE_SIZE

        return "".join(
            self.get_row(curr_y)[
                square_x * self.SQUARE_SIZE : square_x * self.SQUARE_SIZE
                + self.SQUARE_SIZE
            ]
            for curr_y in range(
                square_y * self.SQUARE_SIZE,
                square_y * self.SQUARE_SIZE + self.SQUARE_SIZE,
            )
        )

    def candidates(self, x: int, y: int) -> List[str]:
        "Return a list of candidates for a given field"

        return [
            candidate
            for candidate in (
                self.ALL_NUMS
                - set(self.get_row(y))
                - set(self.get_col(x))
                - set(self.get_square(x, y))
            )
        ]

    def iter_rows(self) -> Iterable[str]:
        "Iterate over all rows of the game"

        for y in range(self.FIELD_SIZE):
            yield self.get_row(y)

    def iter_cols(self) -> Iterable[str]:
        "Iterate over all columns of the game"

        for x in range(self.FIELD_SIZE):
            yield self.get_col(x)

    def iter_squares(self) -> Iterable[str]:
        "Iterate over all square blocks of the game"

        for x, y in product(tee(range(0, self.FIELD_SIZE, self.SQUARE_SIZE))):
            yield self.get_square(x, y)

    def check(self, item: str) -> bool:
        """
        Check if a given item (row, column or square) contains all Numbers
        defined in self.ALL_NUMS
        """

        return set(item) == self.ALL_NUMS

    def is_complete(self) -> bool:
        "Check if the game is completed"

        return all(
            (
                all(self.check(row) for row in self.iter_rows()),
                all(self.check(col) for col in self.iter_cols()),
                all(self.check(square) for square in self.iter_squares()),
            )
        )

    def solve(self, start_at: int = 0, debug: bool = False) -> Iterable[Sudoku]:
        """
        Solve the sudoku puzzle with backtracking and recursively call solve.
        This function returns all possible solutions to a sudoku as a generator.
        """
        for position, num in enumerate(self.game[start_at:], start=start_at):
            if num in self.ALL_NUMS:  # Field already taken
                continue

            if debug:
                print("pos", position)

            y, x = divmod(position, self.FIELD_SIZE)
            candidates = self.candidates(x, y)

            if not candidates:
                if debug:
                    print("No candidates left")
                return

            for candidate in sorted(candidates):
                if debug:
                    print("candidate", candidate)
                    print(
                        "new game",
                        self.game[:position]
                        + str(candidate)
                        + self.game[position + 1 :],
                    )
                    print("old game", self.game)
                    input("Press any key to execute the next step.")
                yield from Sudoku(
                    self.game[:position] + candidate + self.game[position + 1 :]
                ).solve(position, debug)

            if debug:
                print("Gone through all candidates")
            return

        if self.is_complete():
            yield self
