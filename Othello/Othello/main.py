#!/usr/bin/env python
# -*- coding: utf-8 -*-

# モジュールのインポート
import algo
from enum import IntFlag, auto
import func
import re
from tqdm import tqdm


# -------------------------------------------------------------------------------
# global variable
# -------------------------------------------------------------------------------
def read_QL():

    value = 0
    key_l = ()

    # 辞書ファイルオープン
    with open("dict.txt", 'r') as f_ql:
        for line in tqdm(f_ql):
            key_l = (re.findall("\(\(.*\)\)", line))
            value = (line[len(key_l[0])+1:-1])

            algo.ql_dic[key_l[0]] = value

    # # 辞書ファイルオープン
    # with open("dict_temp.txt", 'w') as f_output:
    #     for k, v in algo.ql_dic.items():
    #         f_output.write("{0},{1}\n".format(k, v))
    #         # print(type(k))

    return True

# -------------------------------------------------------------------------------
# main()
# -------------------------------------------------------------------------------


def main():

    print("<- Game Start ->")

    player1 = 0
    player2 = 0
    draw = 0

    func.DBG_PRINT = func.D_print.D_NOTHING
    func.DBG_PRINT = func.D_print.D_ALL

    # 学習用の試行回数
    for i in tqdm(range(1000000)):
        # オセロ開始
        # ret = func.paly_Othello(func.Player.Q_L, func.Player.FIRST)
        # ret = func.paly_Othello(func.Player.Q_L, func.Player.RANDUM)
        ret = func.paly_Othello(func.Player.Q_L, func.Player.Q_L)

        if ret == 1:
            player1 += 1
        elif ret == 2:
            player2 += 1
        else:
            draw += 1

        if(i % 1000 == 0):
            func.DBG_PRINT = func.D_print.D_NOTHING
            func.DBG_PRINT = func.D_print.D_ALL
            print("Result:player1:{0}, player2:{1}, draw:{2}" .format(
                player1, player2, draw))
            player1 = 0
            player2 = 0
            draw = 0
        else:
            func.DBG_PRINT = func.D_print.D_ALL
            func.DBG_PRINT = func.D_print.D_NOTHING

    print("Result:player1:{0}, player2:{1}, draw:{2}" .format(
        player1, player2, draw))

    # 辞書ファイルオープン
    with open("dict.txt", 'w') as f_output:
        for k, v in algo.q_dic.items():
            f_output.write("{0},{1}\n" .format(k, v))

    print("\n")
    print("<- Q Learn ->")
    print("\n")

    # Q学習結果読み込み
    read_QL()

    # Q学習結果確認

    # func.DBG_PRINT = func.D_print.D_ALL
    func.DBG_PRINT = func.D_print.D_PLAY
    func.DBG_PRINT = func.D_print.D_NOTHING

    player1 = 0
    player2 = 0
    draw = 0
    for i in tqdm(range(10000)):
        # オセロ開始
        # ret = func.paly_Othello(func.Player.Q_L_ACT, func.Player.PLAYER)
        ret = func.paly_Othello(func.Player.Q_L_ACT, func.Player.RANDUM)

        if ret == 1:
            player1 += 1
        elif ret == 2:
            player2 += 1
        else:
            draw += 1

    print("player1:{0}, player2:{1}, draw:{2}" .format(player1, player2, draw))

    print("<- Game E n d ->")


# 実行
if __name__ == '__main__':
    main()
