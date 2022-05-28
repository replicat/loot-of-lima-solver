from __future__ import annotations

import pulp as pl


class LootOfLimaBoard:
    def __init__(self, info: list | None = None):
        self.players: tuple = ("a", "b", "c", "d", "e", "public", "loot")

        self._info: list = info or []
        self._problem = pl.LpProblem()

    def add_info(self, info: list):
        self._info.append(info)
