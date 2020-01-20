#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chainer
import chainer.functions as F   # パラメータを持たない関数
import chainer.links as L       # パラメータを持つ関数
from chainer import Function, gradient_check, Variable, optimizers, serializers, utils
from chainer import computational_graph as c
import numpy as np

import func
import random

# ------------------------------------------------------------------------------
# Network definition
# パラメータを持つ層（Link）をまとめておくためのクラス？？


class MLP(chainer.Chain):

    def __init__(self, n_in, n_units, n_out):
        print("n_in:{0}, n_units:{1}, n_out:{2}".format(n_in, n_units, n_out))
        # パラメータを持つ層の登録
        super(MLP, self).__init__(
            l1=L.Linear(n_in, n_units),  # first layer
            l2=L.Linear(n_units, n_units),  # second layer
            l3=L.Linear(n_units, n_units),  # Third layer
            l4=L.Linear(n_units, n_out),  # output layer
        )

    def __call__(self, x, t=None, train=False):
        # データを受け取った際のforward計算を書く
        h = F.leaky_relu(self.l1(x))
        h = F.leaky_relu(self.l2(h))
        h = F.leaky_relu(self.l3(h))
        h = self.l4(h)

        if train:
            # ロス関数
            return F.mean_squared_error(h, t)
        else:
            return h

    def get(self, x):
        # input x as float, output float
        return self.predict(Variable(np.array([x]).astype(np.float32).reshape(1, 1))).data[0][0]


class DQNPlayer:
    def __init__(self, turn, name="DQN", e=1, dispPred=False):
        self.name = name
        self.myturn = turn
        in_layer = 16       # 入力層
        # mid_layer = 324     # 中間層
        mid_layer = 162     # 中間層
        out_layer = 16      # 出力層
        self.model = MLP(in_layer, mid_layer, out_layer)

        # 学習率
        lr = 0.01

        # 勾配降下法の手法設定(SGDほか、MomentumSGD, RMSprop, Adam)
        # 学習曲線（ロスカーブが変わってくる）
        self.optimizer = optimizers.SGD()
        # self.optimizer = optimizers.SGD(lr)

        self.optimizer.setup(self.model)
        self.e = e
        self.gamma = 0.95
        self.dispPred = dispPred
        self.last_move = None
        self.last_board = None
        self.last_pred = None
        self.totalgamecount = 0
        self.rwin, self.rlose, self.rdraw, self.rmiss = 1, -1, 0, -1.5

    def act(self, board):

        self.last_board = board.clone()
        x = np.array([board.board], dtype=np.float32).astype(np.float32)

        pred = self.model(x)
        if self.dispPred:
            print("---Debug---")
            print(x)
            print(pred.data)

        acts = board.get_possible_pos(self.myturn)
        if self.dispPred:
            print("acts", acts)
        if acts[0] == -1:
            return acts[0]

        self.last_pred = pred.data[0, :]
        act = int(np.argmax(pred.data, axis=1))
        if self.dispPred:
            print("act_argmax:", act)

        if self.e > 0.2:  # decrement epsilon over time
            self.e -= 1/(20000)
        if random.random() < self.e:
            i = random.randrange(len(acts))
            act = acts[i]
            if self.dispPred:
                print("last_random:", act)

        # print("act", act)
        # 打ってはだめなところに打った場合
        if act != -1:
            i = 0
            while not act in acts:
            # while board.board[act] != func.EMPTY:
                # print("Wrong Act "+str(board.board)+" with "+str(act))
                self.learn(self.last_board, act, -1, self.last_board)
                x = np.array([board.board], dtype=np.float32).astype(
                    np.float32)
                pred = self.model(x)
                # print("pred.data", pred.data)
                act = int(np.argmax(pred.data, axis=1))
                i += 1
                if i > 10:
                    # print("Exceed Pos Find"+str(board.board)+" with "+str(act))
                    acts = self.last_board.get_possible_pos(self.myturn)
                    act = acts[random.randrange(len(acts))]

        if self.dispPred:
            print("last_act:", act)
        self.last_move = act
        # self.last_pred=pred.data[0,:]
        return act

    def getGameResult(self, board):
        r = 0
        if self.last_move is not None:
            if self.dispPred:
                print("getGameResult:", self.last_move)
                print("board.winner:", board.winner)

            if board.winner is None:
                self.learn(self.last_board, self.last_move, 0, board)
            else:
                # if board.board == self.last_board.board:
                #     self.learn(self.last_board, self.last_move,
                #                self.rmiss, board)
                #     if self.dispPred:
                #         print("<< miss >> ")
                if board.winner == self.myturn:
                    self.learn(self.last_board, self.last_move,
                               self.rwin, board)
                    if self.dispPred:
                        print("<< win >> ")
                elif board.winner != func.DRAW:
                    self.learn(self.last_board, self.last_move,
                               self.rlose, board)
                    if self.dispPred:
                        print("<< lose >> ")
                else:  # DRAW
                    self.learn(self.last_board, self.last_move,
                               self.rdraw, board)
                    if self.dispPred:
                        print("<< draw >> ")
                self.totalgamecount += 1
                self.last_move = None
                self.last_board = None
                self.last_pred = None

    def learn(self, s, a, r, fs):
        if fs.winner is not None:
            maxQnew = 0
        else:
            x = np.array([fs.board], dtype=np.float32).astype(np.float32)
            maxQnew = np.max(self.model(x).data[0])
        update = r+self.gamma*maxQnew
        # print(('Prev Board:{} ,ACT:{}, Next Board:{}, Get Reward {}, Update {}').format(s.board,a,fs.board,r,update))
        # print(('PREV:{}').format(self.last_pred))
        self.last_pred[a] = update

        x = np.array([s.board], dtype=np.float32).astype(np.float32)
        t = np.array([self.last_pred], dtype=np.float32).astype(np.float32)
        if self.dispPred:
            print("x={0}".format(x))
            print("t={0}".format(t))

        # 勾配を初期化
        self.model.zerograds()

        # 順方向に計算して誤差を算出
        loss = self.model(x, t, train=True)

        # 勾配の計算（微分）
        loss.backward()

        # パラメータの更新
        self.optimizer.update()
        # print(('Updated:{}').format(self.model(x).data))
        # print (str(s.board)+"with "+str(a)+" is updated from "+str(pQ)+" refs MAXQ="+str(maxQnew)+":"+str(r))
        # print(self.q)
