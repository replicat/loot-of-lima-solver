from __future__ import annotations

import pulp as pl

from enums import Direction, Terrain
from info import Info, RangeInfo

# Currently only available for 5-players game


class Board:
    def __init__(self, info: list[Info] | None = None):
        # preset variables
        self.players: tuple = ("a", "b", "c", "d", "e", "public", "loot")
        self.max_slot: int = 8 * 3

        # info available
        self._info: list[Info] = info or []

        # lp problem
        self._problem = pl.LpProblem(sense=pl.LpMaximize)
        self._slots: dict[tuple, pl.LpVariable] = pl.LpVariable.dicts(
            name="Slots",
            indices=[(p, s) for p in self.players for s in range(self.max_slot)],
            cat="Binary",
        )

        # init aggregate
        self._aggregated: dict[tuple, float] = {}
        self._count: int = 0
        self._init_aggregate()

    def _init_aggregate(self):
        self._aggregated = {(p, s): 0.0 for p in self.players for s in range(self.max_slot)}
        self._count = 0

    def _get_slots(self, player: str, terrain: Terrain, start: Direction, end: Direction) -> list[pl.LpVariable]:
        if terrain == Terrain.ALL:
            return [
                slot
                for terrain in (Terrain.BEACH, Terrain.FOREST, Terrain.MOUNTAIN)
                for slot in self._get_slots(player, terrain, start, end)
            ]

        # separate slots by terrain
        terrain_slots = {
            Terrain.BEACH: [self._slots[(player, slot)] for slot in range(0, 8)],
            Terrain.FOREST: [self._slots[(player, slot)] for slot in range(8, 16)],
            Terrain.MOUNTAIN: [self._slots[(player, slot)] for slot in range(16, 24)],
        }

        # translate direction to position
        start_pos = start.value
        end_pos = end.value

        if end_pos <= start_pos:
            return terrain_slots[terrain][start_pos:8] + terrain_slots[terrain][0:end_pos]
        else:
            return terrain_slots[terrain][start_pos:end_pos]

    def print(self):
        if self._count <= 0:
            if self._problem.status == pl.LpStatusNotSolved:
                print("Not solved")
            elif self._problem.status == pl.LpStatusInfeasible:
                print("No solution found")
            return

        print("========================================")
        for player in self.players:
            print(player)
            print("----------------------------------------")
            for slot in range(self.max_slot):
                print(f"{self._aggregated[(player, slot)] / self._count:.2f}", end=" ")
                if slot in (7, 15, 23):
                    print()
            print("========================================")
        print(f"Total Iterations: {self._count}")

    def solve(self, max_iterations: int = 100):
        self._init_aggregate()

        # all slots must present once and only once
        for slot in range(self.max_slot):
            self._problem.addConstraint(pl.lpSum(self._slots[(player, slot)] for player in self.players) == 1)

        # each real player have a total of 4 slots
        for player in ("a", "b", "c", "d", "e"):
            self._problem.addConstraint(pl.lpSum(self._slots[(player, slot)] for slot in range(self.max_slot)) == 4)

        # public & loot each have a total of 2 slots
        for player in ("public", "loot"):
            self._problem.addConstraint(pl.lpSum(self._slots[(player, slot)] for slot in range(self.max_slot)) == 2)

        # constraints from info
        for info in self._info:
            if isinstance(info, RangeInfo):
                self._problem.addConstraint(
                    pl.lpSum(self._get_slots(info.player, info.terrain, info.start, info.end)) == info.amount
                )

        for _ in range(max_iterations):
            # solve once
            self._problem.solve(pl.PULP_CBC_CMD(msg=0))
            if self._problem.status != pl.LpStatusOptimal:
                break

            # add to aggregate
            for player in self.players:
                for slot in range(self.max_slot):
                    self._aggregated[(player, slot)] += pl.value(self._slots[(player, slot)])
            self._count += 1

            # add constraint to prevent same solution
            solution = [
                self._slots[(player, slot)]
                for player in self.players
                for slot in range(self.max_slot)
                if pl.value(self._slots[(player, slot)]) == 1
            ]
            self._problem.addConstraint(pl.lpSum(solution) <= self.max_slot - 1)


if __name__ == "__main__":
    info = [
        RangeInfo(player="a", terrain=Terrain.MOUNTAIN, start=Direction.NORTH, end=Direction.SOUTH, amount=4),
        RangeInfo(player="b", terrain=Terrain.FOREST, start=Direction.NORTH, end=Direction.SOUTH, amount=4),
        RangeInfo(player="c", terrain=Terrain.ALL, start=Direction.NORTH, end=Direction.SOUTH, amount=4),
        RangeInfo(player="d", terrain=Terrain.ALL, start=Direction.SOUTH, end=Direction.NORTH, amount=4),
        RangeInfo(player="d", terrain=Terrain.FOREST, start=Direction.EAST, end=Direction.WEST, amount=2),
        RangeInfo(player="d", terrain=Terrain.MOUNTAIN, start=Direction.EAST, end=Direction.WEST, amount=2),
        RangeInfo(player="e", terrain=Terrain.ALL, start=Direction.SOUTH, end=Direction.NORTH, amount=4),
        RangeInfo(player="e", terrain=Terrain.BEACH, start=Direction.SOUTH, end=Direction.SOUTH, amount=2),
        RangeInfo(player="e", terrain=Terrain.FOREST, start=Direction.SOUTH, end=Direction.SOUTH, amount=0),
        RangeInfo(player="public", terrain=Terrain.BEACH, start=Direction.SOUTH, end=Direction.SOUTHWEST, amount=1),
        RangeInfo(player="public", terrain=Terrain.BEACH, start=Direction.WEST, end=Direction.NORTHWEST, amount=1),
    ]
    board = Board(info)
    board.solve()
    board.print()