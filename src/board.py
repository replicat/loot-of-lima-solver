from __future__ import annotations

import pulp as pl


class LootOfLimaBoard:
    def __init__(self, info: list | None = None):
        self.players: tuple = ("a", "b", "c", "d", "e", "public", "loot")
        self.max_slot: int = 8 * 3

        self._info: list = info or []

        self._problem = pl.LpProblem(sense=pl.LpMaximize)
        self._slots: dict = pl.LpVariable.dicts(
            name="Slots",
            indices=(self.players, range(self.max_slot)),
            cat="Binary",
        )

    def add_info(self, info: list):
        self._info.append(info)

    def print(self):
        print("================================")
        for player in self.players:
            print(player)
            print("--------------------------------")
            for slot in range(self.max_slot):
                print(int(pl.value(self._slots[player][slot])), end=" ")
                if slot in (7, 15, 23):
                    print()
            print("================================")
        print(f"Board State: {pl.LpStatus[self._problem.status]}")

    def solve(self):
        # all slots must present once and only once
        for slot in range(self.max_slot):
            self._problem.addConstraint(pl.lpSum(self._slots[player][slot] for player in self.players) == 1)

        # each real player have a total of 4 slots
        for player in ("a", "b", "c", "d", "e"):
            self._problem.addConstraint(pl.lpSum(self._slots[player][slot] for slot in range(self.max_slot)) == 4)

        # public & loot each have a total of 2 slots
        for player in ("public", "loot"):
            self._problem.addConstraint(pl.lpSum(self._slots[player][slot] for slot in range(self.max_slot)) == 2)

        self._problem.solve()


if __name__ == "__main__":
    board = LootOfLimaBoard()
    board.solve()
    board.print()
