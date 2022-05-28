from __future__ import annotations

import enum
import random

import pulp as pl
import tabulate

from . import exceptions


class Board:
    """Representation of a game board."""

    def __init__(
        self,
        players: tuple,
        terrains: enum.Enum,
        directions: enum.Enum,
    ):
        """Constructor of `Board` class.

        Args:
            players (tuple): Tuple of players.
            terrains (enum.Enum): Enum on types of terrain.
            directions (enum.Enum): Enum on directions.
        """
        self._players: tuple = players
        self._terrains: enum.Enum = terrains
        self._directions: enum.Enum = directions

        self.locations: dict[tuple, pl.LpVariable] = pl.LpVariable.dicts(
            name="Locations",
            indices=[(p, t, d) for p in self.players for t in self.terrains for d in self.directions],
            cat="Binary",
        )
        for v in self.locations.values():
            v.setInitialValue(random.randint(0, 1))

    @property
    def players(self) -> tuple:
        return self._players

    @property
    def terrains(self) -> enum.Enum:
        return self._terrains

    @property
    def directions(self) -> enum.Enum:
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

    def get_locations(self, player: str, terrain: str, start: int, end: int) -> list[pl.LpVariable]:
        if player not in self.players:
            raise exceptions.PlayerNotFoundException()

        if terrain not in self.terrains:
            raise exceptions.TerrainNotFoundException()

        if start not in self.directions or end not in self.directions:
            raise exceptions.DirectionNotFoundException()

        if start >= end:
            dirs = list(range(start, len(self.directions) + 1)) + list(range(1, end))
        else:
            dirs = list(range(start, end))

        return [self.locations[(player, self.terrains(terrain), self.directions(d))] for d in dirs]
