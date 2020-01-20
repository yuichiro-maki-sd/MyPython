#!/usr/bin/env python
# -*- coding: utf-8 -*-

import algo
from inspect import currentframe
from enum import IntFlag, auto
import random
import re


class Player(IntFlag):
    PLAYER = auto()
    FIRST = auto()
    RANDUM = auto()
    CORNER = auto()
    MINMAX = auto()
    Q_L_ACT = auto()
    Q_L = auto()


class D_print(IntFlag):
    D_NOTHING = auto()
    D_PLAY = auto()
    D_ALL = auto()


# デバッグプリントの初期値
DBG_PRINT = D_print.D_NOTHING

# ボードサイズ
board_size = 4

# オセロ開始


def paly_Othello(player1, player2):
    global DBG_PRINT
    ret = True
    last_t = ()

    # デッキ作成
    board_l = set_board()

    skip_cnt = 0
    while (skip_cnt < 2):

        # デッキ表示
        display_board(board_l)

        # プレイヤーのターン
        # 駒が打てるか確認
        (end_f, hit_l) = board_check(board_l, 0)
        chkprint(hit_l)
        if(0 < len(hit_l)):
            skip_cnt = 0
            # プレイヤーのアクション選択
            (a_ret, p1_last_t) = p_action(board_l, hit_l, 0, player1)

        else:
            skip_cnt += 1
            if end_f == True:
                break
            else:
                if int(D_print.D_ALL) <= int(DBG_PRINT):
                    print("< player1 will be skipped. >")

        # デッキ表示
        display_board(board_l)

        # コンピューターのターン
        # 駒が打てるか確認
        (end_f, hit_l) = board_check(board_l, 1)
        chkprint(hit_l)
        if(0 < len(hit_l)):
            skip_cnt = 0
            # コンピューターのアクション選択
            (a_ret, p2_last_t) = p_action(board_l, hit_l, 1, player2)

        else:
            skip_cnt += 1
            if end_f == True:
                break
            else:
                if int(D_print.D_ALL) <= int(DBG_PRINT):
                    print("< player2 will be skipped. >")

    # 結果表示
    ret = display_result(board_l)
    if int(D_print.D_PLAY) <= int(DBG_PRINT):
        if ret == 1:
            print("player1 Wins!")
        elif ret == 2:
            print("player2 Wins!")
        else:
            print("Draw..")

    chkprint(p1_last_t)
    chkprint(p2_last_t)
    p1_q = 0xFF
    p2_q = 0xFF
    # player1 Wins!
    if ret == 1:
        if len(p1_last_t) != 0:
            p1_q = 1
        if len(p2_last_t) != 0:
            p2_q = -1
    # player2 Wins!
    elif ret == 2:
        if len(p1_last_t) != 0:
            p1_q = -1
        if len(p2_last_t) != 0:
            p2_q = 1
    # Draw
    else:
        if len(p1_last_t) != 0:
            p1_q = -1
        if len(p2_last_t) != 0:
            p2_q = 1

    # プレイヤー1の辞書更新
    if(p1_q != 0xFF):
        pQ = algo.q_dic.get(p1_last_t, 0)
        val = pQ + algo.alpha * ((p1_q + algo.gamma * 0) - pQ)
        chkprint(pQ, val)
        algo.q_dic[p1_last_t] = val

    # プレイヤー2の辞書更新
    if(p2_q != 0xFF):
        pQ = algo.q_dic.get(p2_last_t, 0)
        val = pQ + algo.alpha * ((p2_q + algo.gamma * 0) - pQ)
        chkprint(pQ, val)
        algo.q_dic[p2_last_t] = val

    # for k, v in algo.q_dic.items():
    #     chkprint(k, v)

    return ret


# ------------------------------------------------------------------------------

def p_action(board_l, hit_l, player, mode):

    a_l = []
    last_t = ()

    # 入力受付
    if (mode == Player.FIRST):
        a_l = algo.act_first(hit_l)
    elif (mode == Player.RANDUM):
        a_l = algo.act_random(hit_l)
    elif (mode == Player.CORNER):
        a_l = algo.act_corner(hit_l)
    elif(mode == Player.MINMAX):
        a_l = algo.act_minmax(hit_l, board_l, player)
    elif(mode == Player.Q_L_ACT):
        a_l = algo.act_ql_act(hit_l, board_l, player)
    elif(mode == Player.Q_L):
        (a_l, last_t) = algo.act_qlearning(hit_l, board_l, player)

    # print("player:{0}, a_l:{1}" .format(player, a_l))

    ret = False
    # 入力エラーの場合リトライする
    for i in range(10):

        # アクション選択
        if (mode == Player.PLAYER):
            if(player == 0):
                action = input("< Your(○) turn. Please enter. (ex. [a,1]) >\n")
            else:
                action = input(
                    "< Your(●) turn. Please enter. (ex. [a,1]) >\n")
        else:
            action = ("{0},{1}".format(a_l[0], a_l[1]))

        # 入力変換
        act_l = action_chg(action)

        # 入力チェック(自分)
        ret = action_check(board_l, act_l, player)
        if (ret != 0):
            break
        else:
            print("< input is incorrect >")

    return (ret, last_t)

# ------------------------------------------------------------------------------


def set_board():
    # ボード初期設定
    board_l = [[0 for i in range(board_size+2)] for j in range(board_size+2)]

    # 初期配置の駒を配置
    cen = int(board_size / 2)
    board_l[cen][cen] = 1
    board_l[cen+1][cen] = 2
    board_l[cen+1][cen+1] = 1
    board_l[cen][cen+1] = 2

    return(board_l)


# ------------------------------------------------------------------------------
def display_board(d_l):

    global DBG_PRINT

    if(D_print.D_PLAY <= DBG_PRINT):

        print("------------",)
        print("  a b c d e f g h",)

        for i in range(board_size):

            print("{0}|".format(i+1), end="")

            for j in range(board_size):
                if (d_l[i+1][j+1] == 0):
                    print("_ ", end="")
                elif (d_l[i+1][j+1] == 1):
                    print("○ ", end="")
                elif (d_l[i+1][j+1] == 2):
                    print("● ", end="")

            print("",)
        print("------------",)

    return (True)


# ------------------------------------------------------------------------------
def action_chg(act):
    a_l = []

    # 入力文字列をリスト格納
    a_l = re.split(',', act)
    if(2 <= len(a_l)):
        # 文字列が十進数かどうかチェック
        if(str.isdecimal(a_l[0])):
            a_l[0] = int(a_l[0])
        else:
            # 行変換
            if (a_l[0] == "a"):
                a_l[0] = 1
            elif (a_l[0] == "b"):
                a_l[0] = 2
            elif (a_l[0] == "c"):
                a_l[0] = 3
            elif (a_l[0] == "d"):
                a_l[0] = 4
            elif (a_l[0] == "e"):
                a_l[0] = 5
            elif (a_l[0] == "f"):
                a_l[0] = 6
            elif (a_l[0] == "g"):
                a_l[0] = 7
            elif (a_l[0] == "h"):
                a_l[0] = 8
            else:
                a_l[0] = board_size + 1

        # 列変換
        # 文字列が十進数かどうかチェック
        if(str.isdecimal(a_l[1])):
            a_l[1] = int(a_l[1])
        else:
            a_l[0] = board_size + 1

    return a_l

# ------------------------------------------------------------------------------


def board_check(board_l, pinpon):
    hit_num = 0
    hit_l = []
    end_f = True

    b_l = [[-1, -1], [0, -1], [1, -1], [-1, 0],
           [1, 0], [-1, 1], [0, 1], [1, 1]]
    p_l = [[1, 2], [2, 1]]

    for l in range(board_size):
        for m in range(board_size):
            a_l = [l+1, m+1]
            hit = 0

            # 範囲チェック
            if (board_size < a_l[0]) or (board_size < a_l[1]):
                continue

            # 既に駒が置かれていないかチェック
            if (board_l[a_l[1]][a_l[0]] != 0):
                continue

            # まだ入力手が残っている（終了ではない）
            end_f = False

            # 周囲に相手の駒がいるかチェック
            for i in range(len(b_l)):
                line = a_l[1] + b_l[i][0]
                col = a_l[0] + b_l[i][1]

                # 相手の駒がいる場合
                if (board_l[line][col] == p_l[pinpon][1]):

                    # 相手の駒をひっくり返せるか確認する
                    for j in range(board_size):
                        line += b_l[i][0]
                        col += b_l[i][1]

                        # 反対側に駒がいない場合
                        if (board_l[line][col] == 0):
                            break
                        # 反対側に自分の駒がいた場合
                        elif (board_l[line][col] == p_l[pinpon][0]):

                            hit = 1
                            hit_l.append([l+1, m+1])
                            break
                            # # 駒をひっくり返す
                            # for k in range(board_size):
                            #     line -= b_l[i][0]
                            #     col -= b_l[i][1]

                            #     if (board_l[line][col] == p_l[pinpon][1]):
                            #         pass
                            #     else:
                            #         break
                if (hit != 0):
                    break

    return (end_f, hit_l)


# ------------------------------------------------------------------------------
def action_check(board_l, a_l, pinpon):
    ret = False
    pieces = 0

    b_l = [[-1, -1], [0, -1], [1, -1], [-1, 0],
           [1, 0], [-1, 1], [0, 1], [1, 1]]
    p_l = [[1, 2], [2, 1]]

    # 要素チェック
    if len(a_l) < 2:
        return False

    # 範囲チェック
    if (board_size < a_l[0]) or (board_size < a_l[1]):
        return False

    # 既に駒が置かれていないかチェック
    if (board_l[a_l[1]][a_l[0]] != 0):
        return False

    # 周囲に相手の駒がいるかチェック
    for i in range(len(b_l)):
        line = a_l[1] + b_l[i][0]
        col = a_l[0] + b_l[i][1]

        # 相手の駒がいる場合
        if (board_l[line][col] == p_l[pinpon][1]):

            # 相手の駒をひっくり返せるか確認する
            for j in range(board_size):
                line += b_l[i][0]
                col += b_l[i][1]

                # 反対側に駒がいない場合
                if (board_l[line][col] == 0):
                    break
                # 反対側に自分の駒がいた場合
                elif (board_l[line][col] == p_l[pinpon][0]):

                    # 駒をひっくり返す
                    for k in range(board_size):
                        line -= b_l[i][0]
                        col -= b_l[i][1]

                        if (board_l[line][col] == p_l[pinpon][1]):
                            board_l[line][col] = p_l[pinpon][0]
                            pieces += 1
                            ret = True
                        else:
                            break

    # ボードに駒を置く
    if(ret == True):
        board_l[a_l[1]][a_l[0]] = p_l[pinpon][0]

    return pieces


# ------------------------------------------------------------------------------
def display_result(d_l):

    global DBG_PRINT
    ret = 0

    player1 = 0
    player2 = 0

    for i in range(board_size):

        for j in range(board_size):

            if (d_l[i + 1][j + 1] == 1):
                player1 += 1
            elif (d_l[i + 1][j + 1] == 2):
                player2 += 1

    chkprint(player1, player2)

    if (player2 < player1):
        ret = 1
    elif (player1 < player2):
        ret = 2
    else:
        ret = 0

    return ret


# -------------------------------------------------------------------------------
# debug print
# https://qiita.com/AnchorBlues/items/f7725ba87ce349cb0382
# -------------------------------------------------------------------------------


def chkprint(*args):
    global DBG_PRINT

    if(int(D_print.D_PLAY) <= int(DBG_PRINT)):
        names = {id(v): k for k, v in currentframe().f_back.f_locals.items()}
        print(', '.join(names.get(id(arg), '???')+' = '+repr(arg)
                        for arg in args))
