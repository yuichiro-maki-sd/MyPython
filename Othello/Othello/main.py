#!/usr/bin/env python
# -*- coding: utf-8 -*-

# モジュールのインポート
import func

# -------------------------------------------------------------------------------
# global variable
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# main()
# -------------------------------------------------------------------------------
def main():

    print("<- Game Start ->")

    player1 = 0
    player2 = 0
    draw = 0

    for i in range(100):
        # オセロ開始
        ret = func.paly_Othello()

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
