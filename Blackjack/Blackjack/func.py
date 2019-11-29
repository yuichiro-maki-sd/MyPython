#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

# ブラックジャック開始


def paly_BJ():
    ret = True

    # カードデッキ作成
    card_l = []
    for j in range(4):
        for i in range(13):
            card = i + 1
            if (card == 1):
                card = "A"
            elif(card == 11):
                card = "J"
            elif(card == 12):
                card = "Q"
            elif(card == 13):
                card = "K"
            else:
                card = str(card)

            card_l.append(card)

    # カードを配る
    diller_l = (random.sample(card_l, 2))
    palyer_l = (random.sample(card_l, 2))

    # カード表示
    list_print(diller_l, palyer_l, True)

    d_val = 0
    p_val = 0
    d_status = True
    p_status = True
    g_status = True
    while (g_status == True):

        if(p_status == True):
            # プレイヤーのアクション選択
            action = input("< Hit(1) or Stand(2) ? >\n")

            if action == "1":
                print("Hit!")
                palyer_l = palyer_l + random.sample(card_l, 1)
            else:
                p_status = False
                print("Stand..")

        # ディラーのカード判定
        val = cal_total(diller_l)
        if (val < 17):
            # 17以下の場合カードを引く
            diller_l = diller_l + random.sample(card_l, 1)
        else:
            d_status = False

        # カード表示
        list_print(diller_l, palyer_l, False)

        # ディラーバースト判定
        d_val = cal_total(diller_l)
        if (21 == d_val):
            print("diller Black Jack! " + str(d_val))
        elif (21 < d_val):
            print("diller burst! " + str(d_val))
            d_val = 0
            g_status = False

        # プレイヤーバースト判定
        p_val = cal_total(palyer_l)
        if (21 == p_val):
            print("player Black Jack! " + str(p_val))
            g_status = False
        elif (21 < p_val):
            print("you burst! " + str(p_val))
            p_val = 0
            g_status = False

        # ゲーム終了判定
        if((p_status != True) and (d_status != True)):
            g_status = False

    # 結果表示
    print("diller: " + str(d_val))
    print("you   : " + str(p_val))
    print("--------------------")

    # 判定
    if(d_val < p_val):
        print("you win!")
    elif (d_val == p_val):
        print("draw..")
    else:
        print("you lose!")

    return ret


# カード表示
def list_print(d_list, p_list, init):

    # ディラーカード表示
    print("--------------------")
    print("diller: ", end="")
    for i in range(len(d_list)):
        if (init == True) and (i == 0):
            print("X,", end="")
        else:
            print(d_list[i] + ",", end="")

    print("\n")

    # プレイヤーカード表示
    print("you   : ", end="")
    for i in range(len(p_list)):
        print(p_list[i] + ",", end="")

    print("\n--------------------")

    return(True)

# カード合計値算出


def cal_total(c_list):

    val = 0
    a_hit = False

    for i in range(len(c_list)):
        if (c_list[i] == "A"):
            val += 1
            a_hit = True
        elif (c_list[i] == "J"):
            val += 10
        elif (c_list[i] == "Q"):
            val += 10
        elif (c_list[i] == "K"):
            val += 10
        else:
            val += int(c_list[i])

    if (a_hit == True) and (val <= 11):
        val += 10

    return(val)
