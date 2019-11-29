#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import random
from tqdm import tqdm       # for tqdm

# デッキを選択する


def select_deck():

    deck_list = []

    # 現在のフォルダパスを取得
    dirname = os.path.dirname(__file__)
    # 初期パラメータファイルパスを設定
    file = dirname + "/parameter/00_init.csv"

    # 入力ファイルオープン
    with open(file, 'r', encoding="utf-8") as f:

        for line in f:
            # 末尾の改行(\n)を除きます。
            if "\n" == line[-1:]:
                line = line[:-1]

            deck_list.append(line)

    # デッキリストを表示、選択
    for i in range(len(deck_list)):
        d_name = deck_list[i].split(",")
        print(" {0}:{1}" .format(i+1, d_name[0]))
    in_line = input("< デッキを選んでください（複数選択可能 選択例：[1,2]） >\n")

    # 選択したデッキ番号をリスト格納
    s_list = in_line.split(',')

    # 選択したデッキ番号からファイル名をリストに格納
    file_list = []
    for i in range(len(s_list)):
        select_list = deck_list[int(s_list[i])-1].split(',')
        file_list.append(select_list[1])

    return file_list


# 王国カードを選択する
def select_card(d_list):

    kingdom_list = []

    # 現在のフォルダパスを取得
    dirname = os.path.dirname(__file__)

    for i in range(len(d_list)):
        # 初期パラメータファイルパスを設定
        file = dirname + "/parameter/" + d_list[i]

        # 入力ファイルオープン
        with open(file, 'r', encoding="utf-8") as f:
            for line in f:
                # 末尾の改行(\n)を除きます。
                if "\n" == line[-1:]:
                    line = line[:-1]

                # 王国カード追加
                kingdom_list.append(line)

    # 各コストの閾値を設定("cost=2,cost=3,cost=4,cost=5")
    acc_list = [2, 2, 2, 2]

    # 王国カード選択処理
    check = False
    while (check == False):
        check = True

        # 選択したデッキより王国カードを10枚取り出す
        k_list = (random.sample(kingdom_list, 10))
        print(k_list)

        cost_list = []
        # 選択した王国カードのコストをリスト化
        for i in range(len(k_list)):
            card = k_list[i].split(",")
            cost_list.append(card[1])

        # 選択した王国カードのコスト閾値をチェック
        for i in range(len(acc_list)):
            if (cost_list.count(str(i+2)) < acc_list[i]):
                check = False
                break

        # print(check)
        # for i in range(len(acc_list)):
        #     print("cost" + str(i+2), cost_list.count(str(i+2)))

    # 表示カードの並び替え
    # print(cost_list)
