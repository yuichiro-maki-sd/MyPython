#!/usr/bin/env python
# -*- coding: utf-8 -*-

import func

# ------------------------------------------------------------------------------
# 手動（人間）
class PlayerHuman:
    def __init__(self, turn):
        self.name = "Human"
        self.myturn = turn

    def act(self, board):
        valid = False
        while not valid:
            try:
                acts = board.get_possible_pos(self.myturn)
                print("acts:", acts)
                if acts[0] == -1:
                    valid = True
                    return acts[0]
                act = input("Where would you like to place " +
                            str(self.myturn) + " (0-XX)? ")
                act = int(act)

                if act in acts:
                    valid = True
                    return act
                else:
                    print("That is not a valid move! Please try again.")
            except Exception as e:
                print(act + "is not a valid move! Please try again.")
        return act

    def getGameResult(self, board):
        if board.winner is not None and board.winner != self.myturn and board.winner != func.DRAW:
            print("I lost...")
