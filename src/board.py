from __future__ import annotations

import random

import pulp as pl
import tabulate

from enums import Direction, Terrain


class Board:
    """Representation of a game board."""

    def __init__(
        self,
        players: tuple,
        terrains: tuple,
        directions: tuple,
    ):
        """Constructor of `Board` class.

        Args:
            players (tuple): Tuple of players.
            terrains (tuple): Tuple of types of terrain.
            directions (tuple): Tuple of directions.
        """
        self._players: tuple = players
        self._terrains: tuple = terrains
        self._directions: tuple = directions

        self.locations: dict[tuple, pl.LpVariable] = pl.LpVariable.dicts(
            name="Player Locations",
            indices=[(p, t, d) for p in self.players for t in self.terrains for d in self.directions],
            cat="Binary",
        )
        for v in self.locations.values():
            v.setInitialValue(random.randint(0, 1))

    @property
    def players(self) -> tuple:
        return self._players

    @property
    def terrains(self) -> tuple:
        return self._terrains

    @property
    def directions(self) -> tuple:
        return self._directions

    def print(self):
        print("=" * 44)
        for p in self.players:
            print(p)
            print("-" * 44)
            table = [[t] + [f"{pl.value(self.locations[(p, t, d)]):f}" for d in self.directions] for t in self.terrains]
            headers = [""] + list(self.directions)
            print(tabulate.tabulate(table, headers, tablefmt="simple", floatfmt=".0f", numalign="center"))
            print("=" * 44)


if __name__ == "__main__":
    board = Board(
        players=("A", "B", "C", "D", "E", "Public", "Loot"),
        terrains=(Terrain.BEACH, Terrain.FOREST, Terrain.MOUNTAIN),
        directions=Direction,
    )
    board.print()
