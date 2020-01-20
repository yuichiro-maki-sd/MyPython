#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# 元ネタ
# https://qiita.com/narisan25/items/e64a5741864d5a3b0db0

import p_a_random
import p_DQN
import p_human
import p_MC
import p_QL
import p_random
import random
from tqdm import tqdm
# ------------------------------------------------------------------------------
EMPTY = 0
PLAYER_W = 1
PLAYER_B = -1
MARKS = {PLAYER_B: "B", PLAYER_W: "W", EMPTY: " "}
DRAW = 2
BOARD_SIZE = 6
BOARD_SURFACE = BOARD_SIZE ** 2
DIMENSION_A = [-BOARD_SIZE - 1, -BOARD_SIZE, -BOARD_SIZE + 1,
               - 1, 1,
               BOARD_SIZE-1, BOARD_SIZE, BOARD_SIZE+1]
DIMENSION_R = [-BOARD_SIZE - 1, -BOARD_SIZE,
               - 1,
               BOARD_SIZE-1, BOARD_SIZE, ]
DIMENSION_L = [-BOARD_SIZE, -BOARD_SIZE + 1,
               1,
               BOARD_SIZE, BOARD_SIZE+1]

# ------------------------------------------------------------------------------


class TTTBoard:

    def __init__(self, board=None, showBoard=False):
        if board == None:
            self.board = []
            for i in range(BOARD_SURFACE):
                # 中心に4つの初期駒を置きます。
                if (i + 1) == BOARD_SURFACE / 2 - BOARD_SIZE / 2:
                    self.board.append(PLAYER_W)
                elif (i + 1) == BOARD_SURFACE / 2 - BOARD_SIZE / 2 + 1:
                    self.board.append(PLAYER_B)
                elif (i + 1) == BOARD_SURFACE / 2 + BOARD_SIZE / 2:
                    self.board.append(PLAYER_B)
                elif (i + 1) == BOARD_SURFACE / 2 + BOARD_SIZE / 2 + 1:
                    self.board.append(PLAYER_W)
                else:
                    self.board.append(EMPTY)
        else:
            self.board = board
        self.winner = None
        self.pass_cnt = 0
        self.display = showBoard

    def get_possible_pos(self, player):
        pos = []
        player_next = -1*player
        # print("player_current", player)
        # print("player_next", player_next)

        for i in range(BOARD_SURFACE):
            # print("i", i)
            if self.board[i] == EMPTY:
                hit = False

                dimension = DIMENSION_A
                if i % BOARD_SIZE == 0:
                    dimension = DIMENSION_L
                elif (i+1) % BOARD_SIZE == 0:
                    dimension = DIMENSION_R

                for j in dimension:
                    x = i + j
                    if (x < 0) or (BOARD_SURFACE <= x):
                        continue

                    # 相手の駒が隣にいる場合
                    if self.board[x] == player_next:
                        # print("j", j)
                        # print("x", x)
                        # 自分の駒がその先にいるか確認する
                        for k in range(BOARD_SIZE-1):
                            l = x + j * k
                            # print("l", l)
                            if (l < 0) or (BOARD_SURFACE <= l):
                                break
                            if self.board[l] == EMPTY:
                                break
                            if self.board[l] == player:
                                hit = True
                                break
                            if abs(j) != BOARD_SIZE:
                                # if (j != BOARD_SIZE) and (j != 1) and (j != -1):
                                if (l % BOARD_SIZE == 0) or ((l + 1) % BOARD_SIZE == 0):
                                    break
                    if hit == True:
                        # print("hit i", i)
                        pos.append(i)
                        break
        if len(pos) == 0:
            pos = [-1]
        return pos

    def print_board(self):
        tempboard = []
        cnt = 0
        # print(self.board)
        for i in self.board:
            piece = MARKS[i]
            if piece == " ":
                piece = cnt
            tempboard.append(piece)
            cnt += 1
        if BOARD_SIZE == 4:
            row = ' {:^2} | {:^2} | {:^2} | {:^2}\n'
            hr = '------------------\n'
            print((hr + row + row + row + row + hr).format(*tempboard))
        if BOARD_SIZE == 6:
            row = ' {:^2} | {:^2} | {:^2} | {:^2} | {:^2} | {:^2}\n'
            hr = '------------------------------------\n'
            print((hr + row + row + row + row + row + row + hr).format(*tempboard))

    def check_winner(self):
        player_w = 0
        player_b = 0
        winner = 0
        for i in range(BOARD_SURFACE):
            if self.board[i] == PLAYER_W:
                player_w += 1
            elif self.board[i] == PLAYER_B:
                player_b += 1
        if player_w < player_b:
            winner = PLAYER_B
        elif player_b < player_w:
            winner = PLAYER_W
        else:
            winner = DRAW

        if self.display:
            print("PLAYER_W:{0}, PLAYER_B:{1}".format(player_w, player_b))

        self.winner = winner

    def move(self, pos, player):
        if pos == -1:
            self.pass_cnt += 1
            # return False
        else:
            self.pass_cnt = 0

            # 自駒を置く
            self.board[pos] = player
            player_next = -1*player

            dimension = DIMENSION_A
            if pos % BOARD_SIZE == 0:
                dimension = DIMENSION_L
            elif (pos+1) % BOARD_SIZE == 0:
                dimension = DIMENSION_R

            for j in dimension:
                x = pos + j
                if (x < 0) or (BOARD_SURFACE <= x):
                    continue

                # 相手の駒が隣にいる場合
                if self.board[x] == player_next:
                    # print("j", j)
                    # print("x", x)
                    # 自分の駒がその先にいるか確認する
                    for k in range(BOARD_SIZE-1):
                        l = x + j * k
                        # print("l", l)
                        if (l < 0) or (BOARD_SURFACE <= l):
                            break
                        if self.board[l] == EMPTY:
                            break
                        if self.board[l] == player:
                            # print("Own", l)
                            # 駒をひっくり返す
                            for m in range(BOARD_SIZE):
                                l = pos + j * (m+1)
                                # print("rev", l)
                                if self.board[l] == player_next:
                                    self.board[l] = player
                                else:
                                    break
                        if abs(j) != BOARD_SIZE:
                            if (l % BOARD_SIZE == 0) or ((l + 1) % BOARD_SIZE == 0):
                                # print("break:", l)
                                break
        if 2 < self.pass_cnt:
            self.pass_cnt = 0
            self.check_winner()
        # self.check_draw(player)

    def clone(self):
        return TTTBoard(self.board.copy(), False)


# ------------------------------------------------------------------------------


class TTT_GameOrganizer:

    def __init__(self, px, po, nplay=1, showBoard=True, showResult=True, stat=100):
        self.player_x = px
        self.player_o = po
        self.nwon = {px.myturn: 0, po.myturn: 0, DRAW: 0}
        self.nplay = nplay
        self.players = (self.player_x, self.player_o)
        self.board = None
        self.disp = showBoard
        self.showResult = showResult
        # self.player_turn = self.player_x
        self.player_turn = self.players[random.randrange(2)]
        self.nplayed = 0
        self.stat = stat

    def progress(self):
        # while self.nplayed < self.nplay:
        for _ in tqdm(range(self.nplay)):
            self.player_turn = self.player_x
            self.board = TTTBoard()
            if self.disp:
                self.board.print_board()

            while self.board.winner == None:
                if self.disp:
                    print("Turn is "+self.player_turn.name)
                act = self.player_turn.act(self.board)

                self.board.move(act, self.player_turn.myturn)

                if self.disp:
                    self.board.print_board()

                if self.board.winner != None:
                    # print("winner:", self.board.winner)
                    # print(self.player_turn.myturn)

                    # notice every player that game ends
                    if self.showResult:
                        print("---------------------------")
                    for i in self.players:
                        i.getGameResult(self.board)
                    if self.board.winner == DRAW:
                        if self.showResult:
                            print("Draw Game")
                    elif self.board.winner == self.player_turn.myturn:
                        out = "Winner : " + self.player_turn.name
                        if self.showResult:
                            print(out)
                    else:
                        self.switch_player()
                        out = "Winner : " + self.player_turn.name
                        if self.showResult:
                            print(out)
                    if self.showResult:
                        print("---------------------------")
                    self.nwon[self.board.winner] += 1
                else:
                    self.switch_player()
                    # Notice other player that the game is going
                    self.player_turn.getGameResult(self.board)

            # 勝利判定
            # self.board.winner = self.board.game_judgment(self.showResult)
            # self.nwon[self.board.winner] += 1

            self.nplayed += 1
            if self.nplayed % self.stat == 0 or self.nplayed == self.nplay:
                print(self.player_x.name+":"+str(self.nwon[self.player_x.myturn])+","+self.player_o.name+":"+str(self.nwon[self.player_o.myturn])
                      + ",DRAW:" + str(self.nwon[DRAW]))

                # 勝利数初期化
                self.nwon[self.player_x.myturn] = 0
                self.nwon[self.player_o.myturn] = 0
                self.nwon[DRAW] = 0

    def switch_player(self):
        if self.player_turn == self.player_x:
            self.player_turn = self.player_o
        else:
            self.player_turn = self.player_x


# ------------------------------------------------------------------------------


def func_main():
    Game_Start()


# ------------------------------------------------------------------------------
def Game_Start():

    # # 人 VS ランダム
    # p1 = p_human.PlayerHuman(PLAYER_W)
    # p2 = p_a_random.PlayerRandom(PLAYER_B)
    # disp = True
    # geme_cnt = 1
    # game = TTT_GameOrganizer(p1, p2, geme_cnt, disp, disp, 100)
    # game.progress()

    # モンテカルロ VS モンテカルロ
    # p1 = p_MC.PlayerMC(PLAYER_W)
    # # p1 = p_a_random.PlayerRandom(PLAYER_W)
    # p2 = p_MC.PlayerMC(PLAYER_B)
    # disp = True
    # geme_cnt = 100
    # game = TTT_GameOrganizer(p1, p2, geme_cnt, disp, True, 100)
    # game.progress()

# ------------------------------------------------------------------------------

    # Q学習 VS なにか
    pQ = p_QL.PlayerQL(PLAYER_W)
    p2 = p_a_random.PlayerRandom(PLAYER_B)
    # p2 = p_MC.PlayerMC(PLAYER_B)
    geme_cnt = 10000000
    disp = False
    # game = TTT_GameOrganizer(p1, p2, geme_cnt, True)
    game = TTT_GameOrganizer(pQ, p2, geme_cnt, disp, disp, 10000)
    game.progress()

    # # p2 = p_human.PlayerHuman(PLAYER_B)
    # pQ.e=0
    # geme_cnt = 10000
    # game = TTT_GameOrganizer(pQ, p2, geme_cnt, disp, disp, 10000)
    # game.progress()

    # # 改良ランダム VS 改良ランダム
    # p1 = p_random.PlayerRandom(PLAYER_W)
    # p2 = p_random.PlayerRandom(PLAYER_B)
    # disp = False
    # geme_cnt = 10000
    # game = TTT_GameOrganizer(p1, p2, geme_cnt, disp, disp, 10000)
    # game.progress()

# ------------------------------------------------------------------------------

    # # DQN VS 改良ランダム
    # disp = False
    # pDQ = p_DQN.DQNPlayer(PLAYER_W, "DQN", 1, disp)
    # p2 = p_random.PlayerRandom(PLAYER_B)
    # # p2 = p_a_random.PlayerRandom(PLAYER_B)
    # geme_cnt = 1000000
    # game = TTT_GameOrganizer(pDQ, p2, geme_cnt, disp, disp, 1000)
    # game.progress()

    # # 効果確認のため値を0にする
    # pDQ.e=0
    # geme_cnt = 10000
    # game = TTT_GameOrganizer(pDQ, p2, geme_cnt, disp, disp, 10000)
    # game.progress()

    # geme_cnt = 1000
    # game = TTT_GameOrganizer(pQ, pDQ, geme_cnt, disp, disp, 1000)
    # game.progress()

    # p2 = p_human.PlayerHuman(PLAYER_B)
    # geme_cnt = 10
    # game = TTT_GameOrganizer(pDQ, p2, geme_cnt, True, True, 100)
    # game.progress()

# ------------------------------------------------------------------------------

    # DQN VS Q学習
    # # pDQ = DQNPlayer(PLAYER_X)
    # pDQ.e = 1
    # pQ = PlayerQL(PLAYER_O, "QL1")
    # geme_cnt = 20000
    # game = TTT_GameOrganizer(pDQ, pQ, geme_cnt, False, False, 1000)
    # game.progress()
