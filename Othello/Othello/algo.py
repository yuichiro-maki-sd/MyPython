#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import func
import main
import random

# 4x4
weight = [
    [2, 1, 1, 2],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [2, 1, 1, 2],
]
mm_alpha = 0
mm_beta = 0

# 入力手辞書
q_dic = {}
ql_dic = {}

# 学習係数（0～1） 0に近いほど目先の報酬を重視する
alpha = 0.5

# 割引率（0～1） 0に近いほど目先の報酬を重視する
gamma = 0.9


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ファースト（最初に見つけた手を指す）


def act_first(hit_l):

    a_l = hit_l[0]

    return (a_l)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ランダム


def act_random(hit_l):

    a_l = random.choice(hit_l)

    return (a_l)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# 角を取ることを優先する、それ以外はランダム


def act_corner(hit_l):

    corner_l = [[1, 1], [1, 4], [4, 1], [4, 4]]

    a_l = random.choice(hit_l)

    for i in range(len(corner_l)):
        if corner_l[i] in hit_l:
            a_l = corner_l[i]
            break

    return (a_l)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Minmaxアルゴリズム


def act_minmax(hit_l, board_l, player):

    limit = 3
    b_l = copy.deepcopy(board_l)

    (a_l, score) = max_level(b_l, limit, player)

    return (a_l)

# ------------------------------------------------------------------------------
# minmaxアルゴリズムに使用するmax値の算出を行う


def max_level(board_l, limit, player):

    global mm_alpha
    global mm_beta

    print("---max_level start--- player:", player)

    score = 1
    score_max = 1
    a_l = []
    buff_l = []

    if (limit < 1):
        return (a_l, score)

    # 入力可能な手を生成
    (end_f, hit_l) = func.board_check(board_l, player)
    if (len(hit_l) == 1):
        return (hit_l[0], score)

    a_l = hit_l[0]
    for i in range(len(hit_l)):

        # 手を打つ
        # hit_temp_l = [hit_l[i][0] - 1, hit_l[i][1] - 1]
        board_temp_l = copy.deepcopy(board_l)
        ret = func.action_check(board_temp_l, hit_l[i], player)
        # print("入力手:{0}, player={1}, ret={2}" .format(hit_l[i], role, ret))
        # func.display_board(board_temp_l)

        # 次の相手の１手（評価が低い手（相手にとって不利な手）を選択する）
        (buff_l, score) = min_level(board_temp_l, (limit-1), player)
        # print("max {0} score:{1}" .format(buff_l, score))

        # if (mm_beta <= score):
        #     break

        if (score_max < score):
            score_max = score
            # if (mm_alpha < score):
            #     mm_alpha = score
            a_l = hit_l[i]

    print("---max_level end---")

    return (a_l, score_max)


# ------------------------------------------------------------------------------
# minmaxアルゴリズムに使用するmin値の算出を行う


def min_level(board_l, limit, player):

    global mm_alpha
    global mm_beta

    # プレイヤーを入れ替えます
    player += 1
    player %= 2

    print("---min_level start--- player:", player)

    score = 1
    score_min = 100
    a_l = []

    if (limit < 1):
        return (a_l, score)

    # 入力可能な手を生成
    (end_f, hit_l) = func.board_check(board_l, player)
    # func.display_board(board_l)
    print(hit_l)
    if (len(hit_l) == 0):
        # score = 1
        score = 2
        return (None, score)
    elif (len(hit_l) == 1):
        return (hit_l[0], score)

    for i in range(len(hit_l)):
        ret = func.action_check(board_l, hit_l[i], player)
        # print("入力手:{0}, player={1}, ret={2}" .format(hit_l[i], player, ret))

        # score = weight[hit_l[i][0]-1][hit_l[i][1]-1]
        # print("min {0} score:{1}" .format(hit_l[i], score))

        # if (score <= mm_alpha):
        #     break

        if (score < score_min):
            score_min = score
            # if (mm_beta < score):
            #     mm_beta = score
            a_l = hit_l[i]

    print("---min_level end---")

    return (a_l, score_min)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Q 学習アルゴリズム


# ------------------------------------------------------------------------------
# Q学習結果で指す


def act_ql_act(hit_l, board_l, player):

    a_l = random.choice(hit_l)

    # for k, v in ql_dic.items():
    #     print("{0},{1}\n" .format(k, v))

    if(player == 0):
        # print("val:", val)

        # リストのボード情報をタプルへ変換
        board_t = chg_tuple(board_l)

        val = 0
        val_min = 1
        val_max = 0
        for hit_list in hit_l:
            key_st = (board_t, tuple(hit_list))
            val = float(ql_dic.get(str(key_st), 1))

            if (val_max < val):
                val_max = val
                a_l = hit_list
                # if(val != 1):
                #     print("val:", val)

            if (val < val_min):
                val_min = val

        # # 選択可能視手がすべて未評価であった場合
        # if (val_min == 1):
        #     # ランダム手とする
        #     a_l = random.choice(hit_l)

    return (a_l)

# ------------------------------------------------------------------------------
# Q学習を行う（指し手はQ学習結果を使用する）


def act_qlearning(hit_l, board_l, player):

    global alpha
    global gamma

    # print("---Q learning start--- player:", player)

    # プレイヤー設定
    pl = copy.deepcopy(player)

    # 手を選択
    a_l = random.choice(hit_l)

    last_t = {}
    if (pl == 0):

        # リストのボード情報をタプルへ変換
        board_t = chg_tuple(board_l)

        value = 0
        val_max = 0

        # 辞書から最善手を探す
        for hit_list in hit_l:

            # 辞書にない手は、評価値:0（最低評価値）とする
            value = q_dic.get((board_t, tuple(hit_list)), 0)

            if int(func.D_print.D_PLAY) <= int(func.DBG_PRINT):
                print("hit_list:{0}, value:{1}" .format(hit_list, value))

            # 未評価の場合
            if value == 0:
                # 選択手とする
                a_l = hit_list
                break

            if val_max < value:
                val_max = value
                a_l = hit_list

        last_t = (board_t, tuple(a_l))

        # 仮定ボードを作成
        board_temp_l = copy.deepcopy(board_l)

        # 入力変換
        action = ("{0},{1}".format(a_l[0], a_l[1]))
        act_l = func.action_chg(action)
        # 自分の手を仮ボードに入力
        ret = func.action_check(board_temp_l, act_l, pl)

        # プレイヤーを入れ替えます
        pl += 1
        pl %= 2

        # print("<< board_temp_l:1 >>")
        # print(pl)
        # func.display_board(board_temp_l)

        # 相手プレイヤーのアクション選択
        (end_f, hit_l) = func.board_check(board_temp_l, pl)

        # ゲーム終了なので、処理を抜ける（ここでは辞書更新を行わない）
        if end_f == True:
            if(int(func.D_print.D_PLAY) <= int(func.DBG_PRINT)):
                print("pl:{0}, end_f:{1}" .format(pl, end_f))
            return (a_l, last_t)

        if len(hit_l) != 0:
            # # 最初の手を選択
            # new_a_l = hit_l[0]
            # ランダムで手を選択
            new_a_l = random.choice(hit_l)
            # 入力変換
            action = ("{0},{1}".format(new_a_l[0], new_a_l[1]))
            act_l = func.action_chg(action)
            # 相手の手を仮ボードに入力
            ret = func.action_check(board_temp_l, act_l, pl)

        # プレイヤーを入れ替えます
        pl += 1
        pl %= 2

        # print("<< board_temp_l:2 >>")
        # print(pl)
        # func.display_board(board_temp_l)

        # 自プレイヤーのアクション選択
        (end_f, hit_l) = func.board_check(board_temp_l, pl)

        # ゲーム終了なので、処理を抜ける（ここでは辞書更新を行わない）
        if end_f == True:
            if(int(func.D_print.D_PLAY) <= int(func.DBG_PRINT)):
                print("pl:{0}, end_f:{1}" .format(pl, end_f))
            return (a_l, last_t)

        # リストのボード情報をタプルへ変換
        new_board_t = chg_tuple(board_temp_l)

        # print(new_board_t, tuple(hit_l))

        q_list = []
        for hit_list in hit_l:
            # if int(func.D_print.D_PLAY) <= int(func.DBG_PRINT):
            #     print(new_board_t, tuple(hit_list))

            # 辞書から評価値を得る
            val = q_dic.get((new_board_t, tuple(hit_list)), 0)
            q_list.append(val)

        # その上で、もっともよい手を探す
        max_q_new = -1
        if len(q_list) != 0:
            max_q_new = max(q_list)

        # 辞書値取得格納
        val = q_dic.get(last_t, 0)

        # 辞書値を更新する
        q = val + alpha * ((0 + gamma * max_q_new) - val)
        if(q != 0):
            q_dic[last_t] = q
            func.chkprint(last_t)
            func.chkprint(val)
            func.chkprint(q)
            func.chkprint(max_q_new)

        if(int(func.D_print.D_PLAY) <= int(func.DBG_PRINT)):
            print("a_l:{0}, q:{1}" .format(a_l, q))
        #     # 辞書表示
        #     for k, v in q_dic.items():
        #         func.chkprint(k, v)

    # print("---Q learning end  --- player:", player)

    return (a_l, last_t)

# 辞書用にボード情報をタプルへ変換する


def chg_tuple(board_l):

    temp_l = []

    for i in range(len(board_l)):
        if (i == 0) or (i == (func.board_size+1)):
            continue
        temp_l += board_l[i]

    # for line_l in board_l:
    #     temp_l += line_l

    return (tuple(temp_l))
