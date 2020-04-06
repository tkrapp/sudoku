from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import ClassVar, Iterable, List


@dataclass
class Sudoku:
    ALL_NUMS: ClassVar = set("123456789")
    CHECKSUM: ClassVar = sum(range(1, 10))

    game: str

    def __getitem__(self, key: int) -> str:
        return self.get_row(key)

    def __iter__(self) -> Iterator:
        return (self[y] for y in range(9))

    def __str__(self) -> str:
        sep = "+-----+-----+-----+"
        rows = [
            f'|{" ".join(row[0:3])}|{" ".join(row[3:6])}|{" ".join(row[6:9])}|'
            for row in self
        ]

        return "\n".join([sep, *rows[0:3], sep, *rows[3:6], sep, *rows[6:9], sep,])

    def get_row(self, y: int) -> str:
        return self.game[9 * y : (9 * y) + 9]

    def get_col(self, x: int) -> str:
        return "".join(row[x] for row in self)

    def get_square(self, x: int, y: int) -> str:
        square_x = x // 3
        square_y = y // 3

        return "".join(
            self[curr_y][square_x * 3 : square_x * 3 + 3]
            for curr_y in range(square_y * 3, square_y * 3 + 3)
        )

    def possible(self, x: int, y: int, num: int) -> bool:
        if not 1 <= num <= 9:
            return False

        number: str = str(num)

        return all(
            (
                number not in self.get_row(y),
                number not in self.get_col(x),
                number not in self.get_square(x, y),
            )
        )

    def candidates(self, x: int, y: int) -> List[int]:
        return [
            int(candidate)
            for candidate in (
                self.ALL_NUMS
                - set(self.get_row(y))
                - set(self.get_col(x))
                - set(self.get_square(x, y))
            )
        ]

    def iter_rows(self) -> Iterable[str]:
        for y in range(9):
            yield self.get_row(y)

    def iter_cols(self) -> Iterable[str]:
        for x in range(9):
            yield self.get_col(x)

    def iter_squares(self) -> Iterable[str]:
        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                yield self.get_square(x, y)

    def check(self, item: str) -> bool:
        return sum(int(num) for num in item) == self.CHECKSUM

    def is_valid(self):
        return all((
            all(self.check(row) for row in self.iter_rows()),
            all(self.check(col) for col in self.iter_cols()),
            all(self.check(square) for square in self.iter_squares()),
        ))

    def solve(self, start_at: int = 0, debug: bool = False) -> Sudoku:
        for position, num in enumerate(self.game[start_at:], start=start_at):
            if num in self.ALL_NUMS:  # Field already taken
                continue

            if debug:
                print("pos", position)

            y, x = divmod(position, 9)
            candidates = self.candidates(x, y)

            if not candidates:
                if debug:
                    print("No candidates left")
                return

            for candidate in candidates:
                if debug:
                    print("candidate", candidate)
                    print(
                        "new game",
                        self.game[:position]
                        + str(candidate)
                        + self.game[position + 1 :],
                    )
                    print("old game", self.game)
                    input("Next")
                yield from Sudoku(
                    f"{self.game[:position]}{candidate}{self.game[position + 1 :]}"
                ).solve(position, debug)
            else:
                if debug:
                    print("Gone through all candidates")
                return

        if self.is_valid():
            yield self
