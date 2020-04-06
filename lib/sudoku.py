from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import ClassVar, Iterable, List


@dataclass
class Sudoku:
    game: str

    ALL_NUMS: ClassVar = set("123456789")
    FIELD_SIZE: ClassVar = 9
    SQUARE_SIZE: Classvar = 3

    def __str__(self) -> str:
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
        return self.game[self.FIELD_SIZE * y : (self.FIELD_SIZE * y) + self.FIELD_SIZE]

    def get_col(self, x: int) -> str:
        return "".join(
            self.game[position]
            for position in range(x, len(self.game), self.FIELD_SIZE)
        )

    def get_square(self, x: int, y: int) -> str:
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
        for y in range(self.FIELD_SIZE):
            yield self.get_row(y)

    def iter_cols(self) -> Iterable[str]:
        for x in range(self.FIELD_SIZE):
            yield self.get_col(x)

    def iter_squares(self) -> Iterable[str]:
        for x in range(0, self.FIELD_SIZE, self.SQUARE_SIZE):
            for y in range(0, self.FIELD_SIZE, self.SQUARE_SIZE):
                yield self.get_square(x, y)

    def check(self, item: str) -> bool:
        return set(item) == self.ALL_NUMS

    def is_valid(self) -> bool:
        return all(
            (
                all(self.check(row) for row in self.iter_rows()),
                all(self.check(col) for col in self.iter_cols()),
                all(self.check(square) for square in self.iter_squares()),
            )
        )

    def solve(self, start_at: int = 0, debug: bool = False) -> Sudoku:
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

        if self.is_valid():
            yield self
