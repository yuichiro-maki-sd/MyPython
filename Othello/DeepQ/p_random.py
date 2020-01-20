#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

# ------------------------------------------------------------------------------
# ランダム手


class PlayerRandom:
    def __init__(self, turn):
        self.name = "Random"
        self.myturn = turn

    def act(self, board):
        acts = board.get_possible_pos(self.myturn)
        # print("acts:", acts)
        i = random.randrange(len(acts))
        # print("acts[i]:", acts[i])
        return acts[i]

    def getGameResult(self, board):
        pass
