from __future__ import annotations

import pulp as pl
import tabulate

from . import board, enums, information


# Currently hardcoded for 5-players standard game
class StandardGame:
    """Representation of the game state."""

    PLAYERS = ("A", "B", "C", "D", "E", "Public", "Loot")
    TERRAINS = enums.StandardTerrain
    DIRECTIONS = enums.StandardDirection
    GAME_RULES = [
        information.RangeInfo(player="A", terrain="A", start=1, end=1, amount=4),
        information.RangeInfo(player="B", terrain="A", start=1, end=1, amount=4),
        information.RangeInfo(player="C", terrain="A", start=1, end=1, amount=4),
        information.RangeInfo(player="D", terrain="A", start=1, end=1, amount=4),
        information.RangeInfo(player="E", terrain="A", start=1, end=1, amount=4),
        information.RangeInfo(player="Public", terrain="A", start=1, end=1, amount=2),
        information.RangeInfo(player="Loot", terrain="A", start=1, end=1, amount=2),
    ]

    def __init__(
        self,
        info: list[information.Info] | None = None,
    ):
        self._info: list[information.Info] = self.GAME_RULES + (info or [])

        self._board = board.Board(
            players=self.PLAYERS,
            terrains=self.TERRAINS,
            directions=self.DIRECTIONS,
        )

        self._problem: pl.LpProblem
        self._aggregated: dict[tuple[str, enums.StandardTerrain, enums.StandardDirection], float]
        self._iteration_count: int

        self._init_solver()

    def _init_solver(self):
        self._problem = pl.LpProblem(sense=pl.LpMaximize)
        self._aggregated = {
            (p, t, d): 0.0 for p in self._board.players for t in self._board.terrains for d in self._board.directions
        }
        self._iteration_count = 0

    def print(self, binary=False):
        if self._iteration_count <= 0:
            if self._problem.status == pl.LpStatusNotSolved:
                print("Not solved")
            elif self._problem.status == pl.LpStatusInfeasible:
                print("No solution found")
            return

        print("=" * 50)
        for p in self._board.players:
            print(p)
            print("-" * 50)
            table = [
                [t] + [f"{self._aggregated[(p, t, d)] / self._iteration_count:f}" for d in self._board.directions]
                for t in self._board.terrains
            ]
            headers = [""] + list(self._board.directions)
            print(tabulate.tabulate(table, headers, tablefmt="simple", floatfmt=".2f", numalign="center"))
            print("=" * 50)
        print(f"Number of iterations: {self._iteration_count}")

    def solve(self, max_iterations: int = 100):
        self._init_solver()

        # constraint: all locations are unique
        for t in self._board.terrains:
            for d in self._board.directions:
                self._problem.addConstraint(
                    pl.lpSum(self._board.locations[(p, t, d)] for p in self._board.players) == 1
                )

        # constraint: from information
        for info in self._info:
            if isinstance(info, information.SingleInfo):
                self._problem.addConstraint(
                    pl.lpSum(self._board.get_location(info.player, info.name)) == int(info.present)
                )
            elif isinstance(info, information.RangeInfo):
                if info.terrain == "A":
                    locs = [
                        loc
                        for sublist in [
                            self._board.get_locations(info.player, t, info.start, info.end)
                            for t in self._board.terrains
                        ]
                        for loc in sublist
                    ]
                else:
                    locs = self._board.get_locations(info.player, info.terrain, info.start, info.end)
                self._problem.addConstraint(pl.lpSum(locs) == info.amount)
            elif isinstance(info, information.LeastTerrainInfo):
                for t in self._board.terrains:
                    if t.value != info.terrain:
                        self._problem.addConstraint(
                            pl.lpSum(self._board.get_locations(info.player, info.terrain, 1, 1))
                            <= pl.lpSum(self._board.get_locations(info.player, t.value, 1, 1))
                        )
            else:
                raise ValueError(f"Unknown information type: {type(info)}")

        # solve until infeasible/max iterations reached
        for _ in range(max_iterations):
            # solve once
            self._problem.solve(pl.PULP_CBC_CMD(msg=0))
            if self._problem.status != pl.LpStatusOptimal:
                break

            # add to aggregate
            for p in self._board.players:
                for t in self._board.terrains:
                    for d in self._board.directions:
                        self._aggregated[(p, t, d)] += pl.value(self._board.locations[(p, t, d)])
            self._iteration_count += 1

            # constraint: prevent same solution
            solution = [
                self._board.locations[(p, t, d)]
                for p in self._board.players
                for t in self._board.terrains
                for d in self._board.directions
                if pl.value(self._board.locations[(p, t, d)]) == 1
            ]
            self._problem.addConstraint(
                pl.lpSum(solution) <= len(self._board.terrains) * len(self._board.directions) - 1
            )

    def get_result(self) -> dict:
        return self._aggregated
