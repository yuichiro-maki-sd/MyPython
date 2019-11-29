#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import re

board_size = 4


# オセロ開始
def paly_Othello():
    ret = True
    a = ["a", "b", "c", "d"]
    b = [1, 2, 3, 4]

    # デッキ作成
    board_l = set_board()

    while (True):
        skip = 0

        # デッキ表示
        display_board(board_l)

        # プレイヤーのターン
        a_ret = 0
        while (a_ret == 0):
            # 駒が打てるか確認
            pieces = board_check(board_l, 0)
            print("Enterable point :{0}" .format(pieces))
            if(0 < pieces):
                skip = 0
                # プレイヤーのアクション選択
                # action = input("< Your(○) turn. Please enter. (ex. [a,1]) >\n")
                action = ("{0},{1}" .format(
                    random.choice(a), random.choice(b)))

                # 入力変換
                act_l = action_chg(action)

                # 入力チェック(自分)
                a_ret = action_check(board_l, act_l, 0)
                if (a_ret == 0):
                    print("< input is incorrect >")
            else:
                print("< You will be skipped. >")
                skip += 1
                break

        # デッキ表示
        display_board(board_l)

        # コンピューターのターン
        a_ret = 0
        while(a_ret == 0):
            # 駒が打てるか確認
            pieces = board_check(board_l, 1)
            print("Enterable point :{0}" .format(pieces))
            if(0 < pieces):
                skip = 0
                # コンピューターのアクション選択
                action = ("{0},{1}" .format(
                    random.choice(a), random.choice(b)))
                # action = input(
                #     "< Computer(●) turn. Please enter. (ex. [a,1]) >\n")

                # 入力変換
                act_l = action_chg(action)

                # 入力チェック(コンピューター)
                a_ret = action_check(board_l, act_l, 1)
                if (a_ret == 0):
                    print("< input is incorrect >")
            else:
                print("< Computer will be skipped. >")
                skip += 1
                break

        if (2 <= skip):
            break

    # デッキ表示
    display_board(board_l)

    # 結果表示
    display_result(board_l)

    return(ret)

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

    print("------",)
    print("  abcd",)

    for i in range(board_size):

        print("{0}|".format(i+1), end="")

        for j in range(board_size):
            if (d_l[i+1][j+1] == 0):
                print("_", end="")
            elif (d_l[i+1][j+1] == 1):
                print("○", end="")
            elif (d_l[i+1][j+1] == 2):
                print("●", end="")

        print("",)
    print("------",)

    return (True)


# ------------------------------------------------------------------------------
def action_chg(act):
    a_l = []

    # 入力文字列をリスト格納
    print(act)
    a_l = re.split(',', act)
    # 行変換
    if (a_l[0] == "a"):
        a_l[0] = 1
    elif (a_l[0] == "b"):
        a_l[0] = 2
    elif (a_l[0] == "c"):
        a_l[0] = 3
    elif (a_l[0] == "d"):
        a_l[0] = 4
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
    pieces = 0
    hit_num = 0

    b_l = [[-1, -1], [0, -1], [1, -1], [-1, 0],
           [1, 0], [-1, 1], [0, 1], [1, 1]]
    p_l = [[1, 2], [2, 1]]

    for l in range(board_size):
        for m in range(board_size):
            a_l = [l+1, m+1]

            # 範囲チェック
            if (board_size < a_l[0]) or (board_size < a_l[1]):
                continue

            # 既に駒が置かれていないかチェック
            if (board_l[a_l[1]][a_l[0]] != 0):
                continue

            hit = 0
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
                            break
                            # # 駒をひっくり返す
                            # for k in range(board_size):
                            #     line -= b_l[i][0]
                            #     col -= b_l[i][1]

                            #     if (board_l[line][col] == p_l[pinpon][1]):
                            #         pass
                            #     else:
                            #         break
            hit_num += hit

    return hit_num


# ------------------------------------------------------------------------------
def action_check(board_l, a_l, pinpon):
    ret = False
    pieces = 0

    b_l = [[-1, -1], [0, -1], [1, -1], [-1, 0],
           [1, 0], [-1, 1], [0, 1], [1, 1]]
    p_l = [[1, 2], [2, 1]]

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

    ret = 0

    p1 = 0
    p2 = 0

    for i in range(board_size):

        for j in range(board_size):

            if (d_l[i + 1][j + 1] == 1):
                p1 += 1
            elif (d_l[i + 1][j + 1] == 2):
                p2 += 1

    if (p2 < p1):
        ret = 2
        print("You are Win!")
    elif (p1 < p2):
        print("You are lose..")
        ret = 1
    else:
        print("Draw..")
        ret = 0

    return (ret)
