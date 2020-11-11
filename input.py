#! /usr/bin/python3


# 入力として与えられたネットから、cell_listとnet_listを作る
# cell_listのi番目には、セルiを含むネットのリストが入っている
# net_listのi番目には、ネットi上に存在するセルのリストが入っている
# ネットは（セル、ピン）のリストとして与えられる
# ネットn = [[c1, p1],[c2, p2],...]


class Input:


    def __init__(self):
        self.net_list = []


    def input(self, fin):
        #
        for line in fin:
