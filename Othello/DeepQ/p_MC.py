#!/usr/bin/env python
# -*- coding: utf-8 -*-

import func
import random

# ------------------------------------------------------------------------------
# モンテカルロ
class PlayerMC:
    def __init__(self, turn, name="MC"):
        self.name = name
        self.myturn = turn

    def getGameResult(self, winner):
        pass

    def win_or_rand(self, board, turn):
        acts = board.get_possible_pos(self.myturn)
        # see only next winnable act
        for act in acts:
            tempboard = board.clone()
            tempboard.move(act, turn)
            # check if win
            if tempboard.winner == turn:
                return act
        i = random.randrange(len(acts))
        return acts[i]

    def trial(self, score, board, act):
        tempboard = board.clone()
        tempboard.move(act, self.myturn)
        tempturn = self.myturn
        while tempboard.winner is None:
            tempturn = tempturn*-1
            # print(tempturn)
            tempboard.move(self.win_or_rand(tempboard, tempturn), tempturn)

        if tempboard.winner == self.myturn:
            score[act] += 1
        elif tempboard.winner == func.DRAW:
            pass
        else:
            score[act] -= 1

    def getGameResult(self, board):
        pass

    def act(self, board):
        acts = board.get_possible_pos(self.myturn)
        # print("acts", acts)
        if len(acts) == 1:
            return acts[0]

        scores = {}
        n = 100


        for act in acts:
            scores[act] = 0
            for i in range(n):
                # print("Try"+str(i))
                self.trial(scores, board, act)

            scores[act] /= n
            # print(scores)

        max_score = max(scores.values())
        for act, v in scores.items():
            if v == max_score:
                # print(str(act)+"="+str(v))
                return act
