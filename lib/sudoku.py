from dataclasses import dataclass
from collections.abc import Iterator
from typing import List

ALL_NUMS = set("123456789")


@dataclass
class Sudoku:
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

    def get_block(self, x: int, y: int) -> str:
        block_x = x // 3
        block_y = y // 3

        return "".join(
            self[curr_y][block_x * 3 : block_x * 3 + 3]
            for curr_y in range(block_y * 3, block_y * 3 + 3)
        )

    def possible(self, x: int, y: int, num: int) -> bool:
        if not 1 <= num <= 9:
            return False

        number: str = str(num)

        return all(
            (
                number not in self.get_row(y),
                number not in self.get_col(x),
                number not in self.get_block(x, y),
            )
        )

    def candidates(self, x: int, y: int) -> List[int]:
        return [
            int(candidate)
            for candidate in (
                ALL_NUMS
                - set(self.get_row(y))
                - set(self.get_col(x))
                - set(self.get_block(x, y))
            )
        ]
