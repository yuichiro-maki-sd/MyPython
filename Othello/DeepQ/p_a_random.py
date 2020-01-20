#!/usr/bin/env python
# -*- coding: utf-8 -*-

import func
import random

# ------------------------------------------------------------------------------
# 改良ランダム手（角が取れたら角を取る）


class PlayerRandom:
    def __init__(self, turn):
        self.name = "alpha_Random"
        self.myturn = turn

    def act(self, board):
        acts = board.get_possible_pos(self.myturn)
        # print("acts:", acts)

        i = random.randrange(len(acts))
        act = acts[i]

        # 角が取れたら角を取る
        for j in acts:
            if (j == 0) or (j == (func.BOARD_SIZE - 1)) or (j == (func.BOARD_SURFACE - func.BOARD_SIZE)) or (j == (func.BOARD_SURFACE - 1)):
                act = j
                break
        # print("act:", act)

        return act

    def getGameResult(self, board):
        pass
